from pydantic import BaseModel

from flymy_comfyui_repo_gen.schemas.BaseComfyWorkflow import BaseComfyWorkflow
from flymy_comfyui_repo_gen.schemas.ComfyRepository import (
    ComfyRepositorySchema,
    InputComfyRepositorySchema,
)
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.ComfyNode import ComfyNodeSchema


class RepoGeneratorConfig(BaseComfyWorkflow):
    comfy_workflow: dict[str, ComfyNodeSchema]
    input_field_paths: list[str]
    comfy_repositories: list[ComfyRepositorySchema]


class DumpRepoGeneratorConfig(RepoGeneratorConfig):
    comfy_repositories: list[InputComfyRepositorySchema]
