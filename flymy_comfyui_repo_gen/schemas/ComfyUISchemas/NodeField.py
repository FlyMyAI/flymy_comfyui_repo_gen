from typing import Any

from pydantic import BaseModel, Field


class NodeField(BaseModel):
    python_type: type
    python_name: str
    comfy_name: str
    node_name: str

    default_value: Any = Field(default=None)
