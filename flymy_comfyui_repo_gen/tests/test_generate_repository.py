from flymy_comfyui_repo_gen.core.generate_repository import generate_repository


def test_generate_repository(base_path):
    generate_repository(
        json_path=base_path / "fixtures" / "test_resolution.json",
        output_dir=base_path / "test_output",
        repo_name="test-repository"
    )
