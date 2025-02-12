# ruff: noqa: E402

from .config import Settings

_config: Settings = Settings.get_config()

from openg2p_fastapi_common.app import Initializer

from .controllers.receive import InternalController
from .controllers.subscribe import SubscribeController
from .controllers.subscribe_confirm import SubscribeConfirmController
from .services.file_store import FileStoreService
from .services.template_renderer import TemplateRendererService


class Initializer(Initializer):
    def initialize(self, **kwargs):
        super().initialize()

        FileStoreService()
        TemplateRendererService()
        InternalController().post_init()
        SubscribeController().post_init()
        SubscribeConfirmController().post_init()

    def init_app(self):
        app = super().init_app()
        app.router.redirect_slashes = False
        return app

    def run_server(self, args):
        _config._server_running = True
        return super().run_server(args)
