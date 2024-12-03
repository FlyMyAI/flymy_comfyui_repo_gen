from typing import Annotated

from pydantic import BaseModel, BeforeValidator, AfterValidator, Field

from flymy_comfyui_repo_gen.core.utils import normalize_u, to_pascal_case, to_snake_case
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.Node import NodeSchema
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField
from flymy_comfyui_repo_gen.schemas.FMARepoConfig import FMARepoConfig


class BaseCodeConfig(BaseModel):
    repo_name: Annotated[
        str, BeforeValidator(normalize_u), AfterValidator(to_pascal_case)
    ]
    repo_settings: FMARepoConfig

    root_src_pypackage: Annotated[
        str,
        Field(alias="repo_name"),
        BeforeValidator(normalize_u),
        AfterValidator(to_snake_case),
    ]

    @property
    def nodes(self):
        node_fields: list[NodeField] = self.repo_settings.fields
        node_names = set(field.node_name for field in node_fields)

        nodes = [
            NodeSchema(
                name=node_name,
                fields=(list(filter(lambda f: f.node_name == node_name, node_fields))),
                node_type=self.repo_settings.edited_comfy_workflow[
                    node_name
                ].class_type,
            )
            for node_name in node_names
        ]
        return nodes
