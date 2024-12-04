import os
import pathlib
import sys

script_path = pathlib.Path(__file__).resolve()
script_parent_dir = script_path.parent.parent.parent
os.environ["PYTHONPATH"] = (
    os.environ.get("PYTHONPATH", "") + ":" + str(script_parent_dir)
)
sys.path.append(str(script_parent_dir))


from flymy_comfyui_repo_gen.scripts.repo_generator import app

if __name__ == "__main__":
    app()
