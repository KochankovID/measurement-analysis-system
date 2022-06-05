from logging.config import dictConfig

from fastapi import FastAPI

from app.api.v1 import type_description_api


def register_routers(app: FastAPI):
    app.include_router(type_description_api.router, tags=["Type description"])


def configure_logging(logger_config: dict):
    dictConfig(logger_config)
