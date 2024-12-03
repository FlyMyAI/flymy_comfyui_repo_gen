from flymy_comfyui_repo_gen.core.code_gen.CodeGenerator import CodeGenerator
from flymy_comfyui_repo_gen.core.code_gen.Types.TypesConfig import TypesConfig


class TypesGenerator(CodeGenerator):
    template_name = "Types.py.j2"

    @property
    def config(self):
        config_map = TypesConfig(
            repo_name=self._repo_name, repo_settings=self._repo_config
        )
        return config_map
