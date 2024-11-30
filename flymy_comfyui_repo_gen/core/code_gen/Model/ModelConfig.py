from flymy_comfyui_repo_gen.core.code_gen.BaseCodeConfig import BaseCodeConfig
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.Node import NodeSchema
from flymy_comfyui_repo_gen.schemas.remap_fielld_set import OUTPUT_NODE_CLASSES_MAP


class ModelConfig(BaseCodeConfig):
    _output_nodes: list[NodeSchema]

    @property
    def output_nodes(self):
        if not hasattr(self, "_output_nodes"):
            self._output_nodes = self.repo_settings.output_nodes
        return self._output_nodes

    @property
    def schema_analog_fields(self) -> list[str]:
        return [OUTPUT_NODE_CLASSES_MAP.get(i.node_type) for i in self.output_nodes]

    @property
    def output_schema(self) -> tuple[tuple[str, NodeSchema]]:
        return tuple(zip(self.schema_analog_fields, self.output_nodes))
