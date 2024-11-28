from pydantic import computed_field

from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.BaseNode import BaseNode
from flymy_comfyui_repo_gen.schemas.remap_fielld_set import COMFY_2_FMA_FIELD_MAP


class ComfyNodeSchema(BaseNode):

    @computed_field
    def flymyai_node_type(self) -> str:
        return COMFY_2_FMA_FIELD_MAP.get(self.class_type, self.class_type)
