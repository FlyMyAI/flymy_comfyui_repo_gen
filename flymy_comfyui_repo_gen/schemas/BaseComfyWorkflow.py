from pydantic import BaseModel

from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.ComfyNode import ComfyNodeSchema


class BaseComfyWorkflow(BaseModel):
    comfy_workflow: dict[str, ComfyNodeSchema]
