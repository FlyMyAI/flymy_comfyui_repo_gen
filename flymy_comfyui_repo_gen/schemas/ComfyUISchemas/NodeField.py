from typing import Any

from pydantic import BaseModel, Field


class NodeField(BaseModel):
    python_type: type
    name: str

    default_value: Any = Field(default=None)
