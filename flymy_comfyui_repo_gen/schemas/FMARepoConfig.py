from pydantic import BaseModel, computed_field, PrivateAttr

from flymy_comfyui_repo_gen.core.exceptions import FieldNotFoundError
from flymy_comfyui_repo_gen.schemas.ComfyRepository import ComfyRepositorySchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.FlyMyComfyUI import FlyMyComfyUINodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.Node import NodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField
from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import RepoGeneratorConfig
from flymy_comfyui_repo_gen.schemas.remap_fielld_set import OUTPUT_NODE_CLASSES_MAP


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

        def find_match(node_name):
            matched = FlyMyComfyUINodeSchema.node_id_regex().match(node_name)
            if not matched:
                raise ValueError(f"id retrieval failed for {node_name}")
            return matched.group(1)

        for field_p in self.input_field_paths:  # 86.inputs.text_field
            parts = field_p.split(".")
            search_id = parts[0]
            field_name = parts[2]

            try:
                parent_node_name: str = next(filter(
                    lambda node_name:
                    find_match(node_name) == search_id,
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

