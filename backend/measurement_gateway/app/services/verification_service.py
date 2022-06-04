from datetime import datetime
from typing import List
from uuid import UUID

from app.models.sqalchemy.verification import Verification
from app.repositories.verification_repository import VerificationRepository


class VerificationService:
    def __init__(self, type_desc_repository: VerificationRepository) -> None:
        self._repository: VerificationRepository = type_desc_repository

    async def get_verifications(self) -> List[Verification]:
        return await self._repository.get_all()

    async def get_verification_by_id(self, type_description_id: UUID) -> Verification:
        return await self._repository.get_by_id(type_description_id)

    async def create_verification(
        self,
        type_description_id: int,
        si_modification: str,
        si_type: str,
        si_verification_date: datetime.date,
    ) -> Verification:
        return await self._repository.add(
            type_description_id=type_description_id,
            si_modification=si_modification,
            si_type=si_type,
            si_verification_date=si_verification_date,
        )
