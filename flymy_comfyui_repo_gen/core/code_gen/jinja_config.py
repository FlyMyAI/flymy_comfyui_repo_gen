from jinja2 import FileSystemLoader, Environment

from flymy_comfyui_repo_gen.core.code_gen import ASSET_PATH
from flymy_comfyui_repo_gen.core.code_gen.filters import j2_remove_prefix

assert ASSET_PATH.is_dir()

j2_environ = Environment(loader=FileSystemLoader(ASSET_PATH / "templates"))

j2_environ.filters["remove_prefix"] = j2_remove_prefix
