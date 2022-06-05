from pathlib import Path

from dependency_injector import containers, providers
from dynaconf import Dynaconf

from app.core.logger import get_logger_config
from app.db.db import Database
from app.db.kafka import Kafka

BASE_DIR: Path = Path(__file__).resolve().parent


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(
        Dynaconf,
        settings_files=[BASE_DIR / "core/config.yml", BASE_DIR / "core/.secrets.yml"],
        environments=True,
        dotenv_path=BASE_DIR / ".env",
        envvar_prefix=False,
    )

    logger_config = providers.Singleton(
        get_logger_config,
        log_file_name=config.provided.PROJECT_NAME,
    )

    db = providers.Singleton(Database, db_url=config.provided.DB_URL)
    kafka = providers.Singleton(Kafka, bootstrap_servers=config.provided.BOOTSTRAP_SERVER)
