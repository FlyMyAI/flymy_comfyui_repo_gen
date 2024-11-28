from typing import Annotated

from pydantic import BaseModel, BeforeValidator, AfterValidator

from flymy_comfyui_repo_gen.core.utils import normalize_u, to_pascal_case
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.Node import NodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField
from flymy_comfyui_repo_gen.schemas.FMARepoConfig import FMARepoConfig


class TypesConfig(BaseModel):
    repo_name: Annotated[str, BeforeValidator(normalize_u), AfterValidator(to_pascal_case)]
    repo_settings: FMARepoConfig

    @property
    def nodes(self):
        node_fields: list[NodeField] = self.repo_settings.fields
        node_names = set(field.node_name for field in node_fields)

        nodes = [
            NodeSchema(
                name=node_name,
                fields=list(filter(lambda f: f.node_name == node_name, node_fields))
            )
            for node_name in node_names
        ]
        return nodes
