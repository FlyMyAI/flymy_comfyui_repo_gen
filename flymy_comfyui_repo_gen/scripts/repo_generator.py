import pathlib

from typer import Typer

from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import RepoGeneratorConfig

app = Typer()


@app.command()
def repo_generator(
    json_path: pathlib.Path,
    output_dir: pathlib.Path
):
    parsed_api = RepoGeneratorConfig.parse_file(json_path)
    output_dir.mkdir(parents=True, exist_ok=True)

