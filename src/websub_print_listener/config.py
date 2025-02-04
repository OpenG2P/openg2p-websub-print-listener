from openg2p_fastapi_common.config import Settings
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(Settings):
    model_config = SettingsConfigDict(
        env_prefix="print_", env_file=".env", extra="allow"
    )

    openapi_title: str = "Print WebSub Listener"
    openapi_description: str = """
    Print WebSub Listener
    ***********************************
    Further details goes here
    ***********************************
    """
    openapi_version: str = __version__

    websub_hub_url: str = "http://localhost:9191/hub"
    websub_subscribe_lease_seconds: int | None = None
    websub_partner_id: str = ""
    websub_api_timeout: int = 10

    # This is a randomly generated secret supplied during installation.
    # Used for https://www.w3.org/TR/websub/#authenticated-content-distribution.
    websub_partner_hub_secret: str = ""

    websub_callback_service_url: str = "http://websub-print-listener"

    websub_auth_token_url: str = (
        "https://keycloak.openg2p.org/realms/master/protocol/openid-connect/token"
    )
    websub_auth_client_id: str = ""
    websub_auth_client_secret: str = ""
    websub_auth_username: str = ""
    websub_auth_password: str = ""
    websub_auth_grant_type: str = "client_credentials"

    websub_topic_group_created: str = "WEBSUB_GROUP_CREATED"
    websub_topic_group_updated: str = "WEBSUB_GROUP_UPDATED"
    websub_topic_indv_created: str = "WEBSUB_INDIVIDUAL_CREATED"
    websub_topic_indv_updated: str = "WEBSUB_INDIVIDUAL_UPDATED"

    websub_topic_prefix_partner_id: bool = True

    indv_template_path: str = ""
    group_template_path: str = ""

    @model_validator(mode="after")
    def change_default_values(self):
        if not self.websub_partner_id:
            self.websub_partner_id = (
                self.websub_auth_username or self.websub_auth_client_id
            )
        if self.websub_topic_prefix_partner_id:
            self.websub_topic_group_created = (
                f"{self.websub_partner_id}/{self.websub_topic_group_created}"
            )
            self.websub_topic_group_updated = (
                f"{self.websub_partner_id}/{self.websub_topic_group_updated}"
            )
            self.websub_topic_indv_created = (
                f"{self.websub_partner_id}/{self.websub_topic_indv_created}"
            )
            self.websub_topic_indv_updated = (
                f"{self.websub_partner_id}/{self.websub_topic_indv_updated}"
            )
        return self
