import pathlib
from typing import Annotated

import typer
from typer import Typer

from flymy_comfyui_repo_gen.core.generate_repository import generate_repository

app = Typer()


@app.command(name="generate_repository")
def generate_repository_entry(
    json_path: Annotated[pathlib.Path, typer.Option(prompt=True)],
    output_dir: Annotated[pathlib.Path, typer.Option(prompt=True)],
    repo_name: Annotated[str, typer.Option(prompt=True)]
):
    generate_repository(json_path, output_dir, repo_name)
