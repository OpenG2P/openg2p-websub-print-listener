from openg2p_fastapi_common.config import Settings
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(Settings):
    model_config = SettingsConfigDict(env_prefix="print_", env_file=".env", extra="allow")

    openapi_title: str = "Print WebSub Listener"
    openapi_description: str = """
    Print WebSub Listener
    ***********************************
    Further details goes here
    ***********************************
    """
    openapi_version: str = __version__

    # Internal Variable
    _server_running: bool = False

    websub_hub_url: str = "http://localhost:9191/hub"
    websub_subscribe_lease_seconds: int | None = None
    websub_partner_id: str = ""
    websub_api_timeout: int = 10

    # This is a randomly generated secret supplied during installation.
    # Used for https://www.w3.org/TR/websub/#authenticated-content-distribution.
    websub_partner_hub_secret: str = ""

    websub_callback_service_url: str = "http://openg2p-websub-print-listener"

    websub_auth_token_url: str = "https://keycloak.openg2p.org/realms/master/protocol/openid-connect/token"
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

    s3_url: str = "http://localhost:9000"
    s3_access_key_id: str = ""
    s3_access_key_secret: str = ""
    s3_bucket_name: str = "cards"

    generated_file_name_pattern: str = 'str(input.uniqueId) + ".pdf"'

    template_folder_path: str = "card_templates"

    template_name_group_created: str = "group_created.html"
    template_name_group_updated: str = "group_updated.html"
    template_name_indv_created: str = "individual_created.html"
    template_name_indv_updated: str = "individual_updated.html"

    receive_response_await_file_gen: bool = False

    @model_validator(mode="after")
    def change_default_values(self):
        if not self.websub_partner_id:
            self.websub_partner_id = self.websub_auth_username or self.websub_auth_client_id
        if self.websub_topic_prefix_partner_id:
            self.websub_topic_group_created = f"{self.websub_partner_id}/{self.websub_topic_group_created}"
            self.websub_topic_group_updated = f"{self.websub_partner_id}/{self.websub_topic_group_updated}"
            self.websub_topic_indv_created = f"{self.websub_partner_id}/{self.websub_topic_indv_created}"
            self.websub_topic_indv_updated = f"{self.websub_partner_id}/{self.websub_topic_indv_updated}"
        return self
