from flymy_comfyui_repo_gen.core.code_gen.CodeGenerator import CodeGenerator
from flymy_comfyui_repo_gen.core.code_gen.Pyproject.PyprojectConfig import (
    PyprojectConfig,
)


class PyprojectGenerator(CodeGenerator):
    template_name = "pyproject.toml.j2"

    @property
    def config(self):
        config_map = PyprojectConfig(
            repo_name=self._repo_name, repo_settings=self._repo_config
        )
        return config_map
