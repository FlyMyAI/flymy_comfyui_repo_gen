import hashlib
from typing import Any

from pydantic import BaseModel, Field

from flymy_comfyui_repo_gen.schemas.remap_fielld_set import COMFY_IMAGE_INPUT_MAPS


class NodeField(BaseModel):
    python_type: type
    python_name: str
    comfy_name: str
    node_name: str

    default_value: Any = Field(default=None)

    def is_transformed_image_input(self):
        for t in COMFY_IMAGE_INPUT_MAPS:
            if self.node_name.startswith(t) and COMFY_IMAGE_INPUT_MAPS[t] == self.comfy_name:
                return True
        return False

    @property
    def infer_value(self):
        if self.is_transformed_image_input():
            return f'load_image("test_{self.node_name}_{self.comfy_name}.jpg")'
        return repr(self.default_value)

    @property
    def python_type_signature_analyzed(self):
        if self.is_transformed_image_input():
            return "np.ndarray"
        return self.python_type.__name__
