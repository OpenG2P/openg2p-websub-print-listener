import logging

from openg2p_fastapi_common.controller import BaseController

from ..config import Settings
from ..schemas.receive_request import WebsubReceiveRequest

_config = Settings.get_config()
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

    def post_receive_group_created(self, receiveRequest: WebsubReceiveRequest):
        _logger.info(
            "Received group created request",
            extra={"props": {"receiveRequest": receiveRequest.model_dump()}},
        )

    def post_receive_group_updated(self, receiveRequest: WebsubReceiveRequest):
        _logger.info(
            "Received group created request",
            extra={"props": {"receiveRequest": receiveRequest.model_dump()}},
        )

    def post_receive_individual_created(self, receiveRequest: WebsubReceiveRequest):
        _logger.info(
            "Received group created request",
            extra={"props": {"receiveRequest": receiveRequest.model_dump()}},
        )

    def post_receive_individual_updated(self, receiveRequest: WebsubReceiveRequest):
        _logger.info(
            "Received group created request",
            extra={"props": {"receiveRequest": receiveRequest.model_dump()}},
        )
