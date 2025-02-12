import asyncio
import io
import logging

import aioboto3
from botocore.exceptions import ClientError, EndpointConnectionError
from openg2p_fastapi_common.service import BaseService

from ..config import Settings

_config: Settings = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class FileStoreService(BaseService):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.aws_session = aioboto3.Session()
        asyncio.run(self.get_or_create_bucket(_config.s3_bucket_name))

    async def save_file(self, name, data: bytes, mimetype=None, **kw):
        file_io = io.BytesIO()
        file_io.write(data)
        file_io.seek(0)
        async with self.get_aws_s3_resource() as s3_res:
            s3_bucket = await s3_res.Bucket(_config.s3_bucket_name)
            s3_obj = await s3_bucket.Object(key=name)
            await s3_obj.upload_fileobj(file_io, ExtraArgs={"ContentType": mimetype} if mimetype else None)

    async def get_or_create_bucket(self, bucket_name: str):
        async with self.get_aws_s3_resource() as s3_res:
            exists = True
            try:
                await s3_res.meta.client.head_bucket(Bucket=bucket_name)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "404":
                    exists = False
            except EndpointConnectionError:
                raise
            if not exists:
                self.aws_s3_bucket = await s3_res.create_bucket(Bucket=bucket_name)

    def get_aws_s3_resource(self):
        return self.aws_session.resource(
            "s3",
            endpoint_url=_config.s3_url,
            aws_access_key_id=_config.s3_access_key_id,
            aws_secret_access_key=_config.s3_access_key_secret,
        )
