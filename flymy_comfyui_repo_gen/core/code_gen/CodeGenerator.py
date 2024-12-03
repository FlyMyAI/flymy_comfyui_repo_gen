from abc import ABC, abstractmethod

import black

from flymy_comfyui_repo_gen.core.code_gen.jinja_config import j2_environ
from flymy_comfyui_repo_gen.schemas.FMARepoConfig import FMARepoConfig


class AbstractCodeGenerator(ABC):
    template_name: str

    @abstractmethod
    def config(self):
        raise NotImplementedError

    def generate(self) -> str:
        jinja_template = j2_environ.get_template(self.template_name)
        return jinja_template.render(config=self.config)


class CodeGenerator(AbstractCodeGenerator, ABC):
    _repo_config: FMARepoConfig
    _repo_name: str

    def __init__(self, repo_config: FMARepoConfig, repo_name: str):
        self._repo_config = repo_config
        self._repo_name = repo_name
