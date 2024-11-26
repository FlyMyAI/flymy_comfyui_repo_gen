import re

from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.BaseNode import BaseNode
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.ComfyNode import ComfyNodeSchema

_NODE_ID_REGEX = re.compile(r"\w+_(\w+)")


class FlyMyComfyUINodeSchema(BaseNode):

    def node_id(self, old_node_id: str):
        return f"{self.class_type}_{old_node_id}"

    @classmethod
    def node_id_regex(cls):
        return _NODE_ID_REGEX

    @classmethod
    def from_comfy(cls, comfy_node: ComfyNodeSchema):
        node_cls = comfy_node.flymyai_node_type
        return cls(
            class_type=node_cls,
            meta=comfy_node.meta,
            inputs=comfy_node.inputs
        )
