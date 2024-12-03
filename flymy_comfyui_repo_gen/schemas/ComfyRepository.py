from typing import Annotated

from pydantic import BaseModel, SecretStr, HttpUrl, BeforeValidator


class ComfyRepositorySchema(BaseModel):
    token: SecretStr | None = None
    manager_capable_name: str | None = None
    url: Annotated[
        HttpUrl | None, BeforeValidator(lambda x: str(x).removesuffix(".git") + ".git")
    ] = None

    @property
    def authorized_git_url(self):
        if self.token is not None:
            return f"{self.url.scheme}://{self.token.get_secret_value()}@{self.url.host}{self.url.path}"
        else:
            return self.url


class InputComfyRepositorySchema(ComfyRepositorySchema):
    token: Annotated[str | None, BeforeValidator(lambda x: x or None)] = None
    manager_capable_name: str | None = None
    url: HttpUrl | None
