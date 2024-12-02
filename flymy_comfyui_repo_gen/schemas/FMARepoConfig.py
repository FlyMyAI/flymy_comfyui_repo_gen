from pydantic import BaseModel, computed_field, PrivateAttr, field_validator

from flymy_comfyui_repo_gen.core.exceptions import FieldNotFoundError
from flymy_comfyui_repo_gen.schemas.ComfyRepository import ComfyRepositorySchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.FlyMyComfyUI import FlyMyComfyUINodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.Node import NodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField
from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import RepoGeneratorConfig
from flymy_comfyui_repo_gen.schemas.remap_fielld_set import OUTPUT_NODE_CLASSES_MAP


def _find_match(node_name):
    matched = FlyMyComfyUINodeSchema.node_id_regex().match(node_name)
    if not matched:
        raise ValueError(f"id retrieval failed for {node_name}")
    return matched.group(1)


class FMARepoConfig(BaseModel):
    input_field_paths: list[str]
    initial_config: RepoGeneratorConfig
    edited_comfy_workflow: dict[str, FlyMyComfyUINodeSchema]

    _fields: list[NodeField] = PrivateAttr(default_factory=list)

    @field_validator("edited_comfy_workflow")
    def remap_comfy_nodes_to_new_ids(cls, value: dict[str, FlyMyComfyUINodeSchema]):
        for k, v in list(value.items()):
            for input_k, input_v in list(v.inputs.items()):
                if isinstance(input_v, list):
                    for idx, probable_comfy_ptr in enumerate(input_v):
                        if not isinstance(probable_comfy_ptr, str):
                            continue
                        some_result = list(filter(
                            lambda x: _find_match(x) == probable_comfy_ptr,
                            value.keys()
                        ))
                        if some_result:
                            value[k].inputs[input_k][idx] = some_result[0]
        return value

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
                    _find_match(node_name) == search_id,
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

    @property
    def comfy_repositories(self):
        return self.initial_config.comfy_repositories

    @property
    def output_nodes(self):
        return [
            NodeSchema(
                fields=[],  # it is not used
                name=name,
                node_type=args.class_type
            )
            for name, args in filter(
                lambda x: x[1].class_type in OUTPUT_NODE_CLASSES_MAP,
                self.edited_comfy_workflow.items()
            )
        ]

