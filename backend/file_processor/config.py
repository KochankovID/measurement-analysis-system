from pathlib import Path

from dynaconf import Dynaconf, LazySettings


settings: LazySettings = Dynaconf(
    settings_files=["config.yml", ".secrets.yaml"],
    environments=True,
    dotenv_path=".env",
    envvar_prefix=False,
)
