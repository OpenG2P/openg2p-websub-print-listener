import logging
from datetime import datetime, timedelta

import httpx
from fastapi import Response
from openg2p_fastapi_common.controller import BaseController

from ..config import Settings

_config: Settings = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class SubscribeController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.router.prefix += "/internal"
        self.router.tags += ["subscribe"]

        self.router.add_api_route(
            "/subscribe/group_created",
            self.post_subscribe_group_created,
            responses={200: {"description": "Subscribed"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/subscribe/group_updated",
            self.post_subscribe_group_updated,
            responses={200: {"description": "Subscribed"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/subscribe/individual_created",
            self.post_subscribe_indv_created,
            responses={200: {"description": "Subscribed"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/subscribe/individual_updated",
            self.post_subscribe_indv_updated,
            responses={200: {"description": "Subscribed"}},
            methods=["POST"],
        )

        self.router.add_api_route(
            "/unsubscribe/group_created",
            self.post_unsubscribe_group_created,
            responses={200: {"description": "Unsubscribed"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unsubscribe/group_updated",
            self.post_unsubscribe_group_updated,
            responses={200: {"description": "Unsubscribed"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unsubscribe/individual_created",
            self.post_unsubscribe_indv_created,
            responses={200: {"description": "Unsubscribed"}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unsubscribe/individual_updated",
            self.post_unsubscribe_indv_updated,
            responses={200: {"description": "Unsubscribed"}},
            methods=["POST"],
        )

        self.access_token: str = None
        self.access_token_expires_after: datetime = None

    async def post_subscribe_group_created(self):
        topic = _config.websub_topic_group_created
        suffix = "receiveGroupCreated"
        return await self.generic_subscribe_request(topic, suffix)

    async def post_subscribe_group_updated(self):
        topic = _config.websub_topic_group_updated
        suffix = "receiveGroupUpdated"
        return await self.generic_subscribe_request(topic, suffix)

    async def post_subscribe_indv_created(self):
        topic = _config.websub_topic_indv_created
        suffix = "receiveIndividualCreated"
        return await self.generic_subscribe_request(topic, suffix)

    async def post_subscribe_indv_updated(self):
        topic = _config.websub_topic_indv_updated
        suffix = "receiveIndividualUpdated"
        return await self.generic_subscribe_request(topic, suffix)

    async def post_unsubscribe_group_created(self):
        topic = _config.websub_topic_group_created
        suffix = "receiveGroupCreated"
        return await self.generic_unsubscribe_request(topic, suffix)

    async def post_unsubscribe_group_updated(self):
        topic = _config.websub_topic_group_updated
        suffix = "receiveGroupUpdated"
        return await self.generic_unsubscribe_request(topic, suffix)

    async def post_unsubscribe_indv_created(self):
        topic = _config.websub_topic_indv_created
        suffix = "receiveIndividualCreated"
        return await self.generic_unsubscribe_request(topic, suffix)

    async def post_unsubscribe_indv_updated(self):
        topic = _config.websub_topic_indv_updated
        suffix = "receiveIndividualUpdated"
        return await self.generic_unsubscribe_request(topic, suffix)

    async def generic_subscribe_request(self, topic, url_suffix, mode="subscribe"):
        auth_token = await self.get_auth_token()
        callback = f"{_config.websub_callback_service_url.rstrip('/')}/internal/{url_suffix}"
        async with httpx.AsyncClient() as client:
            res = await client.post(
                _config.websub_hub_url,
                data={
                    "hub.topic": topic,
                    "hub.callback": callback,
                    "hub.mode": mode,
                    "hub.lease_seconds": _config.websub_subscribe_lease_seconds,
                    "hub.secret": _config.websub_partner_hub_secret,
                },
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=_config.websub_api_timeout,
            )
            res.raise_for_status()
        return Response()

    async def generic_unsubscribe_request(self, topic, url_suffix, mode="unsubscribe"):
        return await self.generic_subscribe_request(topic, url_suffix, mode=mode)

    async def get_auth_token(self):
        if (
            self.access_token
            and self.access_token_expires_after
            and self.access_token_expires_after > datetime.now()
        ):
            return self.access_token
        async with httpx.AsyncClient() as client:
            res = await client.post(
                _config.websub_auth_token_url,
                data={
                    "client_id": _config.websub_auth_client_id,
                    "client_secret": _config.websub_auth_client_secret,
                    "username": _config.websub_auth_username,
                    "password": _config.websub_auth_password,
                    "grant_type": _config.websub_auth_grant_type,
                },
                timeout=_config.websub_api_timeout,
            )
            res.raise_for_status()
            res = res.json()
            self.access_token = res.get("access_token", None)
            self.access_token_expires_after = datetime.now() + timedelta(seconds=res.get("expires_in", None))
        return self.access_token
