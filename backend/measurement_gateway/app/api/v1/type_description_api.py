from typing import List
from uuid import UUID

import aiofiles
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, UploadFile
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.containers import Container
from app.db.kafka import Kafka
from app.models.views.file_process_message import VerificationView
from app.models.views.type_description import (TypeDescriptionForm,
                                               TypeDescriptionView)
from app.repositories.type_description_repository import \
    TypeDescriptionNotFoundError
from app.services.type_description_service import TypeDescriptionService

router = InferringRouter()


@cbv(router)
class TypeDescriptionCBV:
    @inject
    def __init__(
            self,
            type_description_service: TypeDescriptionService = Depends(
                Provide[Container.type_description_service]
            ),
    ):
        self.type_description_service = type_description_service

    @router.get("/type_description")
    async def get_list(
            self,
    ) -> List[TypeDescriptionView]:
        return await self.type_description_service.get_type_descriptions()

    @router.get("/type_description/{type_id}")
    async def get(
            self,
            type_id: UUID,
    ) -> TypeDescriptionView:
        try:
            return await self.type_description_service.get_type_description_by_id(
                type_id
            )
        except TypeDescriptionNotFoundError as e:
            raise HTTPException(status_code=404, detail="Item not found") from e

    @router.post("/type_description", status_code=status.HTTP_201_CREATED)
    async def add(
            self,
            type_description: TypeDescriptionForm,
    ) -> TypeDescriptionView:
        return await self.type_description_service.create_type_description(
            **type_description.dict()
        )

    @router.post("/type_description/file_upload", status_code=status.HTTP_201_CREATED)
    @inject
    async def add_file(
            self,
            file: UploadFile,
            kafka: Kafka = Depends(Provide[Container.kafka]),
    ):
        async with aiofiles.open(f"files/{file.filename}", 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        await kafka.send_message("raw-files", VerificationView(file_name=file.filename))
