import os
import sys
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class _UUDEXSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='UUDEX_')

    host: str = 'localhost'
    port: int = 443
    client_cert_dir: str
    ca_cert: str
    upload_dir: str
    log_level: str = 'INFO'
    api_path: str = '/api'
    secret_key: str

    @field_validator('ca_cert', 'client_cert_dir')
    @classmethod
    def validate_path(cls, v) -> str:
        if not Path(v).expanduser().exists():
            raise ValueError(f"Path {v} does not exist")
        return v



env_file = Path(os.environ.get("UUDEX_ENV_FILE", ".env"))

if not env_file.exists():
    print(f"Environment file {env_file} not found.")
    sys.exit(-1)

UUDEXSettings = _UUDEXSettings(_env_file=env_file) # type: ignore

Path(UUDEXSettings.upload_dir).expanduser().mkdir(parents=True, exist_ok=True)
