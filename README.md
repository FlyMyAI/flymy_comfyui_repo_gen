# ComfyUI Repository Generator

This project provides a set of scripts to generate a wrapper repository for the Flymy.ai service.

## Features

- **Workflow Configuration**: Generate `resolution.json`, a configuration file for repository creation.
- **Repository Generation**: Create a repository structure including files for testing, pipeline setup, and inference.

## Installation

To get started, install the package:

If you use pip:
```bash
pip install -e .
```

If you use poetry:
```bash
poetry install
```

# Usage
## Step 0: Create input directory

Create `playground/` dir on the same level as `pyproject.toml` (root of the current repository) and put `workflow_api.json` there.

To obtain `workflow_api.json` of your pipeline turn on dev mode of a ComfyUI and download it via ComfyUI frontend.

## Step 1: Generate Workflow Configuration

Run the following command to generate the `playground/resolution.json` file, which serves as the configuration for repository generation:

```bash
python flymy_comfyui_repo_gen/scripts/main.py process_workflow_api
```

You'll see:

1. `Enter workflow_api.json path [some default will be here]:` - 
if you performed `Step 0` as it's presented - press ENTER

2. `Enter output json path [playground/resolution.json]:` - 
if you performed `Step 0` as it's presented - press ENTER

3. `Do any fields from node "SOME_NODE_ID" need to be added? [y]: ` - 
if you input an empty string/`y` it will include Node config from `workflow_api.json` into the input schema

4. `Include 'SOME_NODE_ID.inputs.SOME_FIELD_NAME' field into the input schema? [y]: ` - 
if you input an empty string/`y` it will include Node.inputs.field from `workflow_api.json` into the input schema.

5. 
```
Verify results: [
    "SOME_NODE_ID.inputs.SOME_FIELD_NAME"
] [Y/n]: 
```
Verify if the result is correct, if it is - press enter button, if it's incorrect - input the `n` symbol and retry the
step 1.
6. `Does your ComfyUI pipeline contain any repositories not previously specified? [y/n]: ` - add ComfyUI nodes to custom_nodes.
7. `Install mode (git (g), ComfyUI-Manager (cm)) [git (g)]: ` - install mode of a node. 
- If it is a node installed with ComfyUI-Manager - input `cm` mode. 
- If the node installed via git - input `g` mode.

| git                                                                                                                                                                                                                                                                                                                                                                	 | ComfyUI-Manager                                                                                                                                                                                                                                                                                      	|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| `Auth token (invisible input, required for private repos) []:` - auth token for git to `git clone` your private repository.`Repository url: ` - http/https url (NOT SSH!) for the custom node repo. Check out our ComfyUI custom nodes [guide](https://github.com/FlyMyAI/ComfyUI-ExampleNode). 	                                                    | `Enter the title of the node that is corresponding to ComfyUI-Manager (checkout https://github.com/ltdrdata/ComfyUI-Manager/blob/main/custom-node-list.json):`-input the ComfyUI-Manager name of custom node repository. 	|

## Step 2: Generate the Repository

After creating the configuration file, generate the repository structure:
```bash
python flymy_comfyui_repo_gen/scripts/main.py generate_repository
```

1. `Enter config JSON path [playground/resolution.json]: ` - JSON path to `resolution.json` generated on the Step 1.
2. `Enter output directory [playground/result]: ` - result repository dir.
3. `Enter repository name [flymy_comfyui_repo]: ` - project name.

The generated repository will contain the following files:

    infer.py:
        A test script to simulate model warm-up and evaluate the pipeline's performance.

    model.py:
        Defines the base model.
        Handles pipeline setup and inference execution.

    Types.py:
        Contains the generated types used for inference operations.

# Contribution
Feel free to open issues or submit pull requests to improve the project.

### Happy generating!