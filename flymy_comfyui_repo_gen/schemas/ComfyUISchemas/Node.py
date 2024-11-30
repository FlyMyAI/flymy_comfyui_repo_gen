from typing import Annotated

from pydantic import BaseModel, AfterValidator

from flymy_comfyui_repo_gen.core.utils import replace_symbols_with_underscore
from flymy_comfyui_repo_gen.schemas.ComfyUISchemas.NodeField import NodeField
from flymy_comfyui_repo_gen.schemas.remap_fielld_set import COMFY_IMAGE_INPUT_MAPS


class NodeSchema(BaseModel):
    fields: list[NodeField]
    name: Annotated[str, AfterValidator(replace_symbols_with_underscore)]
    node_type: Annotated[str, AfterValidator(replace_symbols_with_underscore)]

    def is_image_input(self):
        return self.node_type in COMFY_IMAGE_INPUT_MAPS

    @property
    def transformed_image_input_field(self):
        if not self.is_image_input():
            raise NotImplemented(
                "This node does not have image input field as an input of pipeline!"
            )

        return next(filter(lambda x: x.is_transformed_image_input(), self.fields))
