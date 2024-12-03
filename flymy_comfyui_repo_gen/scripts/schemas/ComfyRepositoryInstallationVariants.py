import enum


class ComfyRepositoryInstallationVariants(enum.StrEnum):
    GIT = "git (g)"
    COMFY_MANAGER = "ComfyUI-Manager (cm)"

    @classmethod
    def from_short(cls, short_data):
        match short_data:
            case "g" | "git" | cls.GIT:
                return cls.GIT
            case "cm" | cls.COMFY_MANAGER:
                return cls.COMFY_MANAGER
            case _:
                raise ValueError(f"Unsupported installation way: {short_data}!")
