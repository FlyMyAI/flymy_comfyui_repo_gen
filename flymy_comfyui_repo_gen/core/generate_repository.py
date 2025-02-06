from concurrent.futures import ThreadPoolExecutor, Future

from pydantic import RootModel

from flymy_comfyui_repo_gen.core.code_gen.Infer.InferGenerator import InferGenerator
from flymy_comfyui_repo_gen.core.code_gen.Model.ModelGenerator import ModelGenerator
from flymy_comfyui_repo_gen.core.code_gen.Pyproject.PyprojectGenerator import (
    PyprojectGenerator,
)
from flymy_comfyui_repo_gen.core.code_gen.Types.TypesGenerator import TypesGenerator
from flymy_comfyui_repo_gen.core.workflow_edit import WorkflowEditor
from flymy_comfyui_repo_gen.schemas.RepoGeneratorConfig import RepoGeneratorConfig
from flymy_comfyui_repo_gen.schemas.ResultRepo import ResultRepo


def generate_repository(json_path, output_dir, repo_name):
    output_dir.mkdir(parents=True, exist_ok=True)
    parsed_api = RepoGeneratorConfig.parse_file(json_path)
    fma_api = WorkflowEditor(parsed_api).remap_fields()
    tasks = {}
    with ThreadPoolExecutor(max_workers=3) as tpe:
        tasks["assets/workflow_api.json"] = tpe.submit(
            lambda: RootModel(fma_api.edited_comfy_workflow).model_dump_json()
        )
        tasks["Types.py"] = tpe.submit(
            TypesGenerator(repo_config=fma_api, repo_name=repo_name).generate
        )
        tasks["model.py"] = tpe.submit(
            ModelGenerator(repo_config=fma_api, repo_name=repo_name).generate
        )
        tasks["infer.py"] = tpe.submit(
            InferGenerator(repo_config=fma_api, repo_name=repo_name).generate
        )
        tasks["__init__.py"] = ""
        awaited = {}
        for file_p, text_or_future in tasks.items():
            text = text_or_future
            if isinstance(text_or_future, Future):
                text = text_or_future.result()
            awaited[file_p] = text
        result_repo = ResultRepo(
            src_files=awaited,
            out_dir=output_dir,
            repo_name=repo_name,
            root_files={
                "pyproject.toml": PyprojectGenerator(
                    repo_config=fma_api, repo_name=repo_name
                ).generate(),
                "README.md": "",
            },
        )
        result_repo.save()
        result_repo.lint()
