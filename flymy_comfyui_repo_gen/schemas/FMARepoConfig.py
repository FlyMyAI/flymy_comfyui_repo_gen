from pydantic import BaseModel, computed_field, PrivateAttr

from flymy_comfyui_repo_gen.core.exceptions import FieldNotFoundError
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.FlyMyComfyUI import FlyMyComfyUINodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField
from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import RepoGeneratorConfig


class FMARepoConfig(BaseModel):
    input_field_paths: list[str]
    initial_config: RepoGeneratorConfig
    edited_comfy_workflow: dict[str, FlyMyComfyUINodeSchema]

    _fields: list[NodeField] = PrivateAttr(default_factory=list)

    @property
    def fields(self) -> list[NodeField]:
        if self._fields:
            return self._fields
        fields = []
        for field_p in self.input_field_paths:  # 86.inputs.text_field
            parts = field_p.split(".")
            search_id = parts[0]
            field_name = parts[2]

            try:
                parent_node_name: str = next(filter(
                    lambda node_name:
                    FlyMyComfyUINodeSchema.node_id_regex().match(node_name).group(1) == search_id,

                    self.edited_comfy_workflow.keys()
                ))
                parent_node = self.edited_comfy_workflow[parent_node_name]
                fields.append(NodeField(
                    python_type=type(parent_node.inputs[field_name]),
                    python_name=f"{parent_node_name}_{field_name}",
                    comfy_name=field_name,
                    default_value=parent_node.inputs[field_name],
                    node_name=parent_node_name
                ))
            except StopIteration as e:
                raise FieldNotFoundError(f"Field {field_p} not found") from e
        self._fields = fields
        return self._fields

