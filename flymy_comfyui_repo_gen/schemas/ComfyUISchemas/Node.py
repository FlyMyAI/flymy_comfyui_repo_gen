from pydantic import BaseModel

from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField


class NodeSchema(BaseModel):
    fields: list[NodeField]
    name: str
