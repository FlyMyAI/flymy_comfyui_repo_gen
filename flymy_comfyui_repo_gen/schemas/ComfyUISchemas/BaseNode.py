from typing import Any

from pydantic import BaseModel, Field


class BaseNode(BaseModel):
    inputs: dict[str, Any]
    class_type: str
    meta: dict[str, str] = Field(validation_alias="_meta", default_factory=dict)
