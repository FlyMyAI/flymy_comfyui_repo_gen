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
    RepoGeneratorConfig,
    DumpRepoGeneratorConfig,
)
from flymy_comfyui_repo_gen.scripts.schemas.inputs import YesOrNo

app = Typer()


BASE_PATH = pathlib.Path(__file__).parent
PROJECT_PATH = pathlib.Path(__import__("flymy_comfyui_repo_gen").__file__).parent


@app.command(name="generate_repository")
def generate_repository_entry(
    json_path: Annotated[pathlib.Path, typer.Option(prompt=True)],
    output_dir: Annotated[pathlib.Path, typer.Option(prompt=True)],
    repo_name: Annotated[str, typer.Option(prompt=True)],
):
    generate_repository(json_path, output_dir, repo_name)


@app.command(name="generate_repository_json")
def generate_repository_json(
    workflow_api_json_path: Annotated[pathlib.Path, typer.Option(prompt=True)] = (
        PROJECT_PATH.parent / "playground" / "workflow_api.json"
    ),
    output_path: Annotated[pathlib.Path, typer.Option(prompt=True)] = (
        PROJECT_PATH.parent / "playground" / "resolution.json"
    ),
    skip_inputs: YesOrNo = YesOrNo.NO,
):
    if not workflow_api_json_path.parent.exists():
        raise ValueError(f"workflow_api.json path does not exist: {output_path}")
    use_confirmation_mode = typer.prompt(
        default=YesOrNo.NO,
        show_default=True,
        type=YesOrNo,
        text="Should we ask about confirmation of a field input",
    )

    default_prompt = lambda txt, input_type, input_default, val_proc, secure=False: typer.prompt(  # noqa
        text=txt,
        confirmation_prompt=use_confirmation_mode,
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
            f"Verify results: {json.dumps(inputs, indent=4)}",
            default=True,
            show_default=True,
        )
    repositories = generate_resolution_repositories(
        default_prompt,
        obtain_done_flag_callback=lambda: typer.confirm(
            "Do you want to input any repository", default=False, show_default=True
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
