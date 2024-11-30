from typing import Annotated

from pydantic import BeforeValidator

from flymy_comfyui_repo_gen.core.code_gen.BaseCodeConfig import BaseCodeConfig
from flymy_comfyui_repo_gen.core.utils import normalize_u


class PyprojectConfig(BaseCodeConfig):
    repo_name: Annotated[str, BeforeValidator(normalize_u)]
