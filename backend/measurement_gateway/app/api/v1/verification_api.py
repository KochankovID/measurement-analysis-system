from typing import List
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.containers import Container
from app.models.views.verification import VerificationForm, VerificationView
from app.repositories.verification_repository import VerificationNotFoundError
from app.services.verification_service import VerificationService

router = InferringRouter()


@cbv(router)
class VerificationCBV:
    @inject
    def __init__(
        self,
        verification_service: VerificationService = Depends(
            Provide[Container.verification_service]
        ),
    ):
        self.verification_service = verification_service

    @router.get("/verification")
    async def get_list(
        self,
    ) -> List[VerificationView]:
        return await self.verification_service.get_verifications()

    @router.get("/verification/{verification_id}")
    async def get(
        self,
        verification_id: UUID,
    ) -> VerificationView:
        try:
            return await self.verification_service.get_verification_by_id(
                verification_id
            )
        except VerificationNotFoundError as e:
            raise HTTPException(status_code=404, detail="Item not found") from e

    @router.post("/verification", status_code=status.HTTP_201_CREATED)
    async def add(
        self,
        type_description: VerificationForm,
    ) -> VerificationView:
        return await self.verification_service.create_verification(
            **type_description.dict()
        )
