import base64
import io
import logging
import os

import jinja2
import magic
import pdfkit
import qrcode
import qrcode.image.svg
from openg2p_fastapi_common.service import BaseService

from ..config import Settings
from ..schemas.receive_data import WebsubReceiveData

_config: Settings = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class TemplateRendererService(BaseService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_files_loader = jinja2.FileSystemLoader(_config.template_folder_path, followlinks=True)
        self.template_env = jinja2.Environment(
            loader=self.template_files_loader, autoescape=jinja2.select_autoescape()
        )
        self.magic_mime = magic.Magic(mime=True)

        self._unsafe_eval = None

        if _config._server_running:
            self.check_if_templates_exist()

    def get_unsafe_eval(self):
        if not self._unsafe_eval:
            self._unsafe_eval = eval
        return self._unsafe_eval

    def check_if_templates_exist(self):
        self.template_env.get_template(_config.template_name_group_created)
        self.template_env.get_template(_config.template_name_group_updated)
        self.template_env.get_template(_config.template_name_indv_created)
        self.template_env.get_template(_config.template_name_indv_updated)

    def render_template(self, template_name: str, input: WebsubReceiveData, **kw) -> str:
        return self.template_env.get_template(template_name).render(
            renderer=self, input=input, config=_config, logger=_logger, **kw
        )

    def render_pdf(self, template_name: str, input: WebsubReceiveData, **kw) -> bytes:
        return pdfkit.from_string(self.render_template(template_name, input, **kw))

    def infer_file_name_from_input(self, input: WebsubReceiveData) -> str:
        unsafe_eval = self.get_unsafe_eval()
        self = self
        input = input
        return unsafe_eval(_config.generated_file_name_pattern)

    def get_binary_template_data(self, template_name: str) -> bytes:
        bin_data = None
        with open(os.path.join(os.fspath(_config.template_folder_path), template_name), "rb") as file:
            bin_data = file.read()
        return bin_data

    def generate_qrcode_binary(
        self,
        data: bytes | str,
        error_correction: int = qrcode.ERROR_CORRECT_M,
        box_size: int = 10,
        border: int = 4,
        image_factory=qrcode.image.svg.SvgPathImage,
        **kw,
    ) -> bytes:
        """
        Qrcode Error Correction integer mapping.
        0 -> ERROR_CORRECT_M
        1 -> ERROR_CORRECT_L
        2 -> ERROR_CORRECT_H
        3 -> ERROR_CORRECT_Q
        """
        if not data:
            return None
        qr_data = qrcode.make(
            data,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            image_factory=image_factory,
            **kw,
        )
        qr_buffer = io.BytesIO()
        qr_data.save(qr_buffer)
        qr_buffer.seek(0)
        return qr_buffer.read()

    def generate_qrcode_htmlsafe(
        self,
        data: bytes | str,
        error_correction: int = qrcode.ERROR_CORRECT_M,
        box_size: int = 10,
        border: int = 4,
        image_factory=qrcode.image.svg.SvgPathImage,
        **kw,
    ):
        return self.convert_bin_to_htmlsafe(
            self.generate_qrcode_binary(
                data,
                error_correction=error_correction,
                box_size=box_size,
                border=border,
                image_factory=image_factory,
                **kw,
            ),
            mimetype="image/svg+xml" if issubclass(image_factory, qrcode.image.svg.SvgImage) else None,
        )

    def convert_bin_to_htmlsafe(self, data: bytes, mimetype: str = None):
        if not data:
            return None
        if not mimetype:
            mimetype = self.infer_mime_type_from_data(data)
        b64_data = base64.b64encode(data).decode()
        return f"data:{mimetype};base64,{b64_data}"

    def infer_mime_type_from_data(self, data: bytes | str):
        if not data:
            return None
        return self.magic_mime.from_buffer(data)
