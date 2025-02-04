from pydantic import BaseModel, ConfigDict


class WebsubReceiveRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
