import logging

from fastapi import Query, Response
from openg2p_fastapi_common.controller import BaseController

from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class SubscribeConfirmController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.prefix += "/internal"
        self.router.tags += ["confirmation"]

        self.router.add_api_route(
            "/receiveGroupCreated",
            self.get_receive_group_created,
            responses={200: {"description": "Group create subscribe confirm"}},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/receiveGroupUpdated",
            self.get_receive_group_updated,
            responses={200: {"description": "Group update subscribe confirm"}},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/receiveIndividualCreated",
            self.get_receive_individual_created,
            responses={200: {"description": "Indv create subscribe confirm"}},
            methods=["GET"],
        )
        self.router.add_api_route(
            "/receiveIndividualUpdated",
            self.get_receive_individual_updated,
            responses={200: {"description": "Indv update subscribe confirm"}},
            methods=["GET"],
        )

    def get_receive_group_created(
        self,
        topic: str = Query(alias="hub.topic"),
        mode: str = Query(alias="hub.mode"),
        reason: str | None = Query(alias="hub.reason", default=None),
        challenge: str | None = Query(alias="hub.challenge", default=None),
    ):
        # TODO: match topic and mode
        return self.generic_subscription_confirmation(topic, mode, reason, challenge)

    def get_receive_group_updated(
        self,
        topic: str = Query(alias="hub.topic"),
        mode: str = Query(alias="hub.mode"),
        reason: str | None = Query(alias="hub.reason", default=None),
        challenge: str | None = Query(alias="hub.challenge", default=None),
    ):
        # TODO: match topic and mode
        return self.generic_subscription_confirmation(topic, mode, reason, challenge)

    def get_receive_individual_created(
        self,
        topic: str = Query(alias="hub.topic"),
        mode: str = Query(alias="hub.mode"),
        reason: str | None = Query(alias="hub.reason", default=None),
        challenge: str | None = Query(alias="hub.challenge", default=None),
    ):
        # TODO: match topic and mode
        return self.generic_subscription_confirmation(topic, mode, reason, challenge)

    def get_receive_individual_updated(
        self,
        topic: str = Query(alias="hub.topic"),
        mode: str = Query(alias="hub.mode"),
        reason: str | None = Query(alias="hub.reason", default=None),
        challenge: str | None = Query(alias="hub.challenge", default=None),
    ):
        # TODO: match topic and mode
        return self.generic_subscription_confirmation(topic, mode, reason, challenge)

    def generic_subscription_confirmation(
        self, topic: str, mode: str, reason: str = None, challenge: str = None
    ):
        if reason:
            _logger.info("Group Create Subscription Success request called.")
        elif challenge:
            _logger.info("Group Create Subscription Verification request called.")
            return Response(content=challenge)
        return Response()
