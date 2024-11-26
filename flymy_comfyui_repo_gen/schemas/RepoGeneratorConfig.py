from pydantic import BaseModel

from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.ComfyNode import ComfyNodeSchema


class RepoGeneratorConfig(BaseModel):
    comfy_workflow: dict[str, ComfyNodeSchema]
    input_field_paths: list[str]
