from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.containers import Container
from app.models.views.type_description import TypeDescriptionForm, TypeDescriptionView
from app.services.type_description_service import TypeDescriptionService

router = InferringRouter()


@cbv(router)
class TypeDescriptionCBV:
    @inject
    def __init__(self, type_description_service: TypeDescriptionService = Depends(
        Provide[Container.type_description_service]
    )):
        self.type_description_service = type_description_service

    @router.get("/type_description")
    async def get_list(
            self,
    ) -> List[TypeDescriptionView]:
        return await self.type_description_service.get_type_descriptions()

    @router.get("/type_description/{type_id}")
    async def get(
            self,
            type_id: int,
    ) -> TypeDescriptionView:
        return await self.type_description_service.get_type_description_by_id(type_id)

    @router.post("/type_description", status_code=status.HTTP_201_CREATED)
    async def add(
            self,
            type_description: TypeDescriptionForm,
    ) -> TypeDescriptionView:
        return await self.type_description_service.create_type_description(
            **type_description.dict()
        )
