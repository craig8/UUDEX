import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #dev: bool = Field(alias="DEV", default=False)
    #x_ssl_cert: str = Field(alias="X-SSL-CERT")
    db_uri: str = Field(alias="postgres_dsn")
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', secrets_dir="secrets")


def get_settings(path: Optional[str] = None) -> Settings:
    global __settings__

    if __settings__ is None and path is None:
        raise ValueError("Settings haven't been created yet!")

    if not __settings__:
        __settings__ = Settings(_env_file=path)    # type: ignore

    return __settings__


__settings__: Optional[Settings] = None

if __name__ == '__main__':
    print(Settings(_env_file='.env-develop',
                   _secrets_dir="secrets").model_dump())    # type: ignore

    print(f"ENV['DEV'] -> {os.environ.get('DEV')}")
