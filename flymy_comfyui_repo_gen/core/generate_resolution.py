import json
import pathlib
import typing
from types import UnionType
from typing import Callable, Any, AnyStr

from pydantic import HttpUrl

from flymy_comfyui_repo_gen.schemas.BaseComfyWorkflow import BaseComfyWorkflow
from flymy_comfyui_repo_gen.schemas.ComfyRepository import (
    ComfyRepositorySchema,
    InputComfyRepositorySchema,
)
from flymy_comfyui_repo_gen.scripts.schemas.ComfyRepositoryInstallationVariants import (
    ComfyRepositoryInstallationVariants,
)
from flymy_comfyui_repo_gen.scripts.schemas.StringEnumChoice import StringEnumChoice
from flymy_comfyui_repo_gen.scripts.schemas.inputs import YesOrNo


def generate_resolution_inputs(
    workflow_api_json: AnyStr,
    request_input_callback: Callable[
        [
            str,  # prompt
            UnionType | type,  # type return
            Any,  # default
            Callable[[Any], Any] | None,  # val proc
            bool,  # secure
        ],
        Any,
    ],
):
    parsing_schema = BaseComfyWorkflow.model_validate(
        dict(comfy_workflow=json.loads(workflow_api_json))
    )
    input_fields = []
    for k, v in parsing_schema.comfy_workflow.items():
        if any(
            map(lambda x: not isinstance(x, list), v.inputs.values())
        ) and request_input_callback(
            f'\nDo any fields from node "{k}" need to be added?',
            YesOrNo,
            YesOrNo.YES,
            None,
            False,
        ):
            for input_k, input_v in v.inputs.items():
                result_schema_name = f"{k}.inputs.{input_k}"
                if not isinstance(input_v, list) and request_input_callback(
                    f"Include '{result_schema_name}' field into the input schema?",
                    YesOrNo,
                    YesOrNo.YES,
                    None,
                    False,
                ):
                    input_fields.append(result_schema_name)
    return input_fields


def generate_resolution_repositories(
    request_input_callback: Callable[
        [
            str,  # prompt
            UnionType | type,  # type return
            Any,  # default
            Callable[[Any], Any] | None,  # val proc
            bool,  # secure
        ],
        Any,
    ],
    obtain_done_flag_callback: Callable[[], bool],
):
    repos = []
    while True:
        if not obtain_done_flag_callback():
            break
        install_way = request_input_callback(
            "Install mode",
            StringEnumChoice(ComfyRepositoryInstallationVariants),
            ComfyRepositoryInstallationVariants.GIT,
            ComfyRepositoryInstallationVariants.from_short,
            False,
        )

        def restrict_empty(*args):
            while True:
                data = request_input_callback(*args)
                if data:
                    return data

        match install_way:
            case ComfyRepositoryInstallationVariants.GIT:
                repos.append(
                    InputComfyRepositorySchema(
                        token=request_input_callback(
                            "Auth token for git (not visible)", str, "", None, True
                        ),
                        url=restrict_empty("Repository url", HttpUrl, None, None),
                    )
                )
            case ComfyRepositoryInstallationVariants.COMFY_MANAGER:
                repos.append(
                    ComfyRepositorySchema(
                        manager_capable_name=restrict_empty(
                            "Enter the title of the node that is corresponding to ComfyUI-Manager "
                            "(checkout https://github.com/ltdrdata/ComfyUI-Manager/blob/main/custom-node-list.json)",
                            str,
                            None,
                            None,
                            False,
                        )
                    )
                )
    return repos
