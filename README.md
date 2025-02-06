# ComfyUI Repository Generator

This project provides a set of scripts to generate a wrapper repository for the Flymy.ai service.

## Features

- **Workflow Configuration**: Generate `resolution.json`, a configuration file for repository creation.
- **Repository Generation**: Create a repository structure, including files for testing, pipeline setup, and inference.

## Installation

To get started, install the package using one of the following methods:

If you use pip:
```bash
pip install -e .
```

If you use poetry:
```bash
poetry install
```

# Usage
## Step 0: Create the input directory

Create a `playground/` directory at the same level as `pyproject.toml` (the root of the current repository) and place your `workflow_api.json` there.

To obtain your pipeline's `workflow_api.json`, enable developer mode in ComfyUI and then download it via the ComfyUI interface.

## Step 1: Generate the Workflow Configuration

Run the following command to generate the `playground/resolution.json` file, which serves as the configuration for repository generation:

```bash
python flymy_comfyui_repo_gen/scripts/main.py process_workflow_api
```

You'll be prompted for input:

1. `Enter workflow_api.json path [some default will be here]:`  
   If you completed Step 0 as described, just press ENTER.

2. `Enter output json path [playground/resolution.json]:`  
   If you completed Step 0 as described, just press ENTER.

3. `Do any fields from node "SOME_NODE_ID" need to be added? [y]:`  
   Press ENTER (or type `y`) to include the node configuration from `workflow_api.json` into the input schema.

4. `Include 'SOME_NODE_ID.inputs.SOME_FIELD_NAME' field into the input schema? [y]:`  
   Press ENTER (or type `y`) to include the specified field from `workflow_api.json` into the input schema.

5. `Verify results: [ "SOME_NODE_ID.inputs.SOME_FIELD_NAME" ] [Y/n]:`  
   If the result is correct, press ENTER. If not, type `n` and retry Step 1.

6. `Does your ComfyUI pipeline contain any repositories not previously specified? [y/n]:`  
   Input `y` if you need to add custom ComfyUI nodes, otherwise `n`.

7. `Install mode (git (g), ComfyUI-Manager (cm)) [git (g)]: `  
   Choose the installation mode for the node:
   - Type `cm` if the node is installed via ComfyUI-Manager.
   - Type `g` if the node is installed from a git repository.

| git                                                                                                                                                                                 | ComfyUI-Manager                                                                                                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Auth token (invisible input, required for private repos) []:`  Enter the auth token for git access.                                                                                | `Enter the title of the node that corresponds to ComfyUI-Manager (checkout https://github.com/ltdrdata/ComfyUI-Manager/blob/main/custom-node-list.json):` Enter the ComfyUI-Manager name of the custom node repository. |
| `Repository url: `  Enter the HTTP/HTTPS URL (NOT SSH!) for the custom node repository. Check out our ComfyUI custom nodes [guide](https://github.com/FlyMyAI/ComfyUI-ExampleNode). |                                                                                                                                                                                                                         |

8. `Does your ComfyUI pipeline requires any files not previously specified? [y/n]: `
    Input `y` if you need to add custom file to the Comfy pipeline.

9. `Enter the file http url:`
    Input the HTTP url of file. The file will be pulled with http get request.

10. `Enter the save path (START WITH ComfyUI/, if the file needs to be saved inside comfy):`

    Input path for file to save. If you need to save the file somewhere inside the ComfyUI's folder - start with `ComfyUI/` prefix,
    for example: `ComfyUI/models/checkpoints/DreamShaperXL_Lightning.safetensors`
    

## Step 2: Generate the Repository

After creating the configuration file, generate the repository structure:

```bash
python flymy_comfyui_repo_gen/scripts/main.py generate_repository
```

You will be prompted for:

1. `Enter config JSON path [playground/resolution.json]: `  
   Provide the path to the `resolution.json` generated in Step 1 (press ENTER if defaults are correct).

2. `Enter output directory [playground/result]: `  
   Specify the output directory for the generated repository (press ENTER for default).

3. `Enter repository name [flymy_comfyui_repo]: `  
   Specify the project name (press ENTER for default).

The generated repository will contain the following files:

- `infer.py`:
  A test script to simulate model warm-up and evaluate the pipeline's performance.

- `model.py`:
  Defines the base model, handles pipeline setup, and executes inference.

- `Types.py`:
  Contains the generated types used for inference operations.

# Contribution
Feel free to open issues or submit pull requests to improve this project.

### Happy generating!

