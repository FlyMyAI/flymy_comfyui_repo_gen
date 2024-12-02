from flymy_comfyui_repo_gen.core.utils import replace_symbols_with_underscore
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.FlyMyComfyUI import FlyMyComfyUINodeSchema
from flymy_comfyui_repo_gen.schemas.FMARepoConfig import FMARepoConfig
from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import RepoGeneratorConfig


class WorkflowEditor:
    def __init__(self, repo_config: RepoGeneratorConfig):
        self._repo_config = repo_config

    def remap_fields(self) -> FMARepoConfig:
        edited_workflow = {}
        for node_id, node in self._repo_config.comfy_workflow.items():
            fma_node = FlyMyComfyUINodeSchema.from_comfy(node)
            edited_workflow[fma_node.node_id(node_id)] = fma_node
        return FMARepoConfig(
            edited_comfy_workflow=edited_workflow,
            input_field_paths=self._repo_config.input_field_paths,
            initial_config=self._repo_config
        )
