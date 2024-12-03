from flymy_comfyui_repo_gen.core.code_gen.CodeGenerator import CodeGenerator
from flymy_comfyui_repo_gen.core.code_gen.Model.ModelConfig import ModelConfig


class ModelGenerator(CodeGenerator):
    template_name = "model.py.j2"

    @property
    def config(self):
        config_map = ModelConfig(
            repo_name=self._repo_name, repo_settings=self._repo_config
        )
        return config_map
