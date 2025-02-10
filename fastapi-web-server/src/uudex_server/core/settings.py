import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)

SETTINGS_FILE = Path(os.environ.get('UUDEX_SETTINGS', '.env')).resolve().as_posix()


class Settings(BaseSettings):
    #dev: bool = Field(alias="DEV", default=False)
    x_ssl_cert: str = Field(alias="X-SSL-CERT")
    db_uri: str = Field(alias="postgres_dsn")
    messagebus_connection: str = Field(alias="messagebus_connection")
    model_config = SettingsConfigDict(env_file=SETTINGS_FILE,
                                      extra='ignore',
                                      secrets_dir="secrets")


def get_settings(path: Optional[str] = None) -> Settings:
    global __settings__

    if __settings__ is None:
        if path is None:
            path = SETTINGS_FILE
        else:
            path = Path(str(path)).expanduser().resolve().as_posix()

        logger.debug(f"Loading settings from: {path}")

        if not Path(path).exists():
            raise ValueError(f"Settings file not found: {path}")

        __settings__ = Settings(_env_file=path)    # type: ignore

    return __settings__


__settings__: Optional[Settings] = None

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print(Settings(_env_file='.env-develop',
                   _secrets_dir="secrets").model_dump())    # type: ignore

    print(f"ENV['DEV'] -> {os.environ.get('DEV')}")
