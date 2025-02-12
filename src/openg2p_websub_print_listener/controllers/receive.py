import asyncio
import logging

from fastapi import Response
from openg2p_fastapi_common.controller import BaseController

from ..config import Settings
from ..schemas.receive_data import WebsubReceiveData
from ..services.file_store import FileStoreService
from ..services.template_renderer import TemplateRendererService

_config: Settings = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class InternalController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.prefix += "/internal"
        self.router.tags += ["receive"]
        self.router.redirect_slashes = False

        self.router.add_api_route(
            "/receiveGroupCreated",
            self.post_receive_group_created,
            responses={200: {"description": "Received"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/receiveGroupUpdated",
            self.post_receive_group_updated,
            responses={200: {"description": "Received"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/receiveIndividualCreated",
            self.post_receive_individual_created,
            responses={200: {"description": "Received"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/receiveIndividualUpdated",
            self.post_receive_individual_updated,
            responses={200: {"description": "Received"}},
            methods=["POST"],
        )

        # Avoiding trailing slash
        self.router.add_api_route(
            "/receiveGroupCreated/",
            self.post_receive_group_created,
            responses={200: {"description": "Received"}},
            methods=["POST"],
            include_in_schema=False,
        )
        self.router.add_api_route(
            "/receiveGroupUpdated/",
            self.post_receive_group_updated,
            responses={200: {"description": "Received"}},
            methods=["POST"],
            include_in_schema=False,
        )
        self.router.add_api_route(
            "/receiveIndividualCreated/",
            self.post_receive_individual_created,
            responses={200: {"description": "Received"}},
            methods=["POST"],
            include_in_schema=False,
        )
        self.router.add_api_route(
            "/receiveIndividualUpdated/",
            self.post_receive_individual_updated,
            responses={200: {"description": "Received"}},
            methods=["POST"],
            include_in_schema=False,
        )

        self._template_renderer_service: TemplateRendererService = None
        self._file_store_service: FileStoreService = None

    @property
    def template_renderer_service(self):
        if not self._template_renderer_service:
            self._template_renderer_service = TemplateRendererService.get_component()
        return self._template_renderer_service

    @property
    def file_store_service(self):
        if not self._file_store_service:
            self._file_store_service = FileStoreService.get_component()
        return self._file_store_service

    async def render_pdf_and_save_file(self, template_name: str, data: WebsubReceiveData):
        file_data = self.template_renderer_service.render_pdf(template_name, data)
        file_name = self.template_renderer_service.infer_file_name_from_input(data)
        await self.file_store_service.save_file(file_name, file_data, mimetype="application/pdf")

    async def post_receive_group_created(self, receive_data: WebsubReceiveData):
        _logger.debug(
            "Received group created request",
            extra={"props": {"receiveRequest": receive_data.model_dump()}},
        )
        coro = self.render_pdf_and_save_file(_config.template_name_group_created, receive_data)
        if _config.receive_response_await_file_gen:
            await coro
        else:
            asyncio.create_task(coro)
        return Response()

    async def post_receive_group_updated(self, receive_data: WebsubReceiveData):
        _logger.debug(
            "Received group updated request",
            extra={"props": {"receiveRequest": receive_data.model_dump()}},
        )
        coro = self.render_pdf_and_save_file(_config.template_name_group_updated, receive_data)
        if _config.receive_response_await_file_gen:
            await coro
        else:
            asyncio.create_task(coro)
        return Response()

    async def post_receive_individual_created(self, receive_data: WebsubReceiveData):
        _logger.debug(
            "Received Individual created request",
            extra={"props": {"receiveRequest": receive_data.model_dump()}},
        )
        coro = self.render_pdf_and_save_file(_config.template_name_indv_created, receive_data)
        if _config.receive_response_await_file_gen:
            await coro
        else:
            asyncio.create_task(coro)
        return Response()

    async def post_receive_individual_updated(self, receive_data: WebsubReceiveData):
        _logger.debug(
            "Received Individual updated request",
            extra={"props": {"receiveRequest": receive_data.model_dump()}},
        )
        coro = self.render_pdf_and_save_file(_config.template_name_indv_updated, receive_data)
        if _config.receive_response_await_file_gen:
            await coro
        else:
            asyncio.create_task(coro)
        return Response()
