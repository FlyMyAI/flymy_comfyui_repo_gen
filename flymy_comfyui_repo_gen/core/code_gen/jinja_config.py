from jinja2 import FileSystemLoader, Environment

from flymy_comfyui_repo_gen.core.code_gen import ASSET_PATH

assert ASSET_PATH.is_dir()

j2_environ = Environment(loader=FileSystemLoader(
    ASSET_PATH / "templates"
))
