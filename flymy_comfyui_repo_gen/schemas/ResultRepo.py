import os
import pathlib
import re
import subprocess
import sys

from pydantic import BaseModel

from flymy_comfyui_repo_gen.core.utils import normalize_u


class ResultRepo(BaseModel):
    src_files: dict[str, str]
    root_files: dict[str, str]

    out_dir: pathlib.Path
    repo_name: str

    @property
    def src_dir(self):
        return self.out_dir / normalize_u(self.repo_name)

    def save(self):
        os.makedirs(str(self.src_dir / "assets"), exist_ok=True)
        for file_p, text in self.src_files.items():
            file_path = (self.src_dir / file_p)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if file_path.exists():
                os.chmod(file_path, mode=0o664)
            file_path.write_text(text)
            os.chmod(file_path, mode=0o664)

        for file_p, text in self.root_files.items():
            file_path = (self.out_dir / file_p)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if file_path.exists():
                os.chmod(file_path, mode=0o664)
            file_path.write_text(text)
            os.chmod(file_path, mode=0o664)

    def lint(self):
        command = f"{sys.executable} -m black --preview {self.src_dir} --exclude {self.src_dir / 'assets'}"
        print(f"Launching: {command}")
        try:
            subprocess.check_call(
                command,
                shell=True, text=True, stderr=subprocess.PIPE
            )
            print(f"Linting completed successfully for {self.src_dir}!")
        except subprocess.CalledProcessError as e:
            print(f"Linting failed with error code {e.returncode}.")
            print(f"Error details: {e.stderr=};\n{e.stdout=}")
            raise
