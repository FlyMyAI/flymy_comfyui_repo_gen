import json
import pathlib
from typing import Annotated

import typer
from typer import Typer

from flymy_comfyui_repo_gen.core.generate_repository import generate_repository
from flymy_comfyui_repo_gen.core.generate_resolution import (
    generate_resolution_inputs,
    generate_resolution_repositories,
)
from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import (
    DumpRepoGeneratorConfig,
)
from flymy_comfyui_repo_gen.scripts.schemas.inputs import YesOrNo

app = Typer()

BASE_PATH = pathlib.Path(__file__).parent
PROJECT_PATH = pathlib.Path(__import__("flymy_comfyui_repo_gen").__file__).parent


@app.command(name="process_workflow_api")
def process_workflow_api(
    workflow_api_json_path: Annotated[
        pathlib.Path, typer.Option(prompt="Enter workflow_api.json path")
    ] = (PROJECT_PATH.parent / "playground" / "workflow_api.json"),
    output_path: Annotated[
        pathlib.Path, typer.Option(prompt="Enter output json path")
    ] = (PROJECT_PATH.parent / "playground" / "resolution.json"),
    skip_inputs: YesOrNo = YesOrNo.NO,
):
    if not workflow_api_json_path.parent.exists():
        raise ValueError(f"workflow_api.json path does not exist: {output_path}")

    default_prompt = lambda txt, input_type, input_default, val_proc, secure=False: typer.prompt(  # noqa
        text=txt,
        confirmation_prompt=YesOrNo.NO,
        show_default=True,
        hide_input=secure,
        type=input_type,
        default=input_default,
        value_proc=val_proc,
        show_choices=True,
    )

    inputs = []
    workflow_api_json = workflow_api_json_path.read_bytes()
    inputs_done = False
    while not inputs_done and not skip_inputs:
        inputs = generate_resolution_inputs(workflow_api_json, default_prompt)
        inputs_done = typer.confirm(
            f"\nVerify results: {json.dumps(inputs, indent=4)}",
            default=True,
            show_default=True,
        )
    repositories = generate_resolution_repositories(
        default_prompt,
        obtain_done_flag_callback=lambda: typer.confirm(
            "\nDoes your ComfyUI pipeline contain any repositories not previously specified?",
            default=None,
            show_default=True,
        ),
    )
    output_path.parent.mkdir(exist_ok=True, parents=True)
    output_path.write_text(
        DumpRepoGeneratorConfig(
            comfy_workflow=json.loads(workflow_api_json),
            input_field_paths=inputs,
            comfy_repositories=repositories,
        ).model_dump_json(indent=4)
    )


@app.command(name="generate_repository")
def generate_repository_entry(
    json_path: Annotated[
        pathlib.Path,
        typer.Option(
            prompt="Enter config JSON path",
        ),
    ] = (PROJECT_PATH.parent / "playground" / "resolution.json"),
    output_dir: Annotated[
        pathlib.Path, typer.Option(prompt="Enter output directory")
    ] = (PROJECT_PATH.parent / "playground" / "result"),
    repo_name: Annotated[
        str, typer.Option(prompt="Enter repository name")
    ] = "flymy_comfyui_repo",
):
    generate_repository(json_path, output_dir, repo_name)
