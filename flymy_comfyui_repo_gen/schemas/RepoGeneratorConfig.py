import pydantic
from pydantic import BaseModel

from flymy_comfyui_repo_gen.schemas.BaseComfyWorkflow import BaseComfyWorkflow
from flymy_comfyui_repo_gen.schemas.ComfyRepository import (
    ComfyRepositorySchema,
    InputComfyRepositorySchema,
)
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.ComfyNode import ComfyNodeSchema


class FilePathSchema(BaseModel):
    pull_uri: pydantic.HttpUrl
    file_path: str
    comfy_relative: bool


class RepoGeneratorConfig(BaseComfyWorkflow):
    comfy_workflow: dict[str, ComfyNodeSchema]
    input_field_paths: list[str]
    comfy_repositories: list[ComfyRepositorySchema]
    extra_files: list[FilePathSchema]


class DumpRepoGeneratorConfig(RepoGeneratorConfig):
    comfy_repositories: list[InputComfyRepositorySchema]
