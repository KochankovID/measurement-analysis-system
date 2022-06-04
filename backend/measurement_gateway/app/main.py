import uvicorn
from dependency_injector.wiring import inject
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.containers import Container
from app.core.init_app import register_routers


@inject
def create_app() -> FastAPI:
    container = Container()
    container.wire(
        packages=[
            "app.api.v1",
        ]
    )

    inner_app = FastAPI(
        title=container.config().PROJECT_NAME,
        description=container.config().PROJECT_DESCRIPTION,
        version=container.config().VERSION,
        contact=container.config().CONTACTS,
        # openapi_tags=settings.TAGS_METADATA,
        default_response_class=ORJSONResponse,
    )

    origins = ["*"]
    inner_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    inner_app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=container.config().ALLOWED_HOSTS
    )

    inner_app.container = container
    register_routers(inner_app)

    @inner_app.on_event("startup")
    async def startup_event():
        await container.kafka().setup()

    return inner_app


app = create_app()

if __name__ == "__main__":
    container = Container()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=container.config().PORT,
        log_config=container.logger_config(),
    )
