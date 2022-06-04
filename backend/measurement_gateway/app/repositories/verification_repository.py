from contextlib import AbstractAsyncContextManager
from datetime import datetime
from typing import Callable, List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sqalchemy.verification import Verification


class VerificationRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> List[Verification]:
        async with self.session_factory() as session:
            type_descriptions = await session.execute(select(Verification))
            return type_descriptions.scalars().all()

    async def get_by_id(self, type_description_id: int) -> Verification:
        async with self.session_factory() as session:
            type_description = await session.get(Verification, type_description_id)
            if not type_description:
                raise VerificationNotFoundError(type_description)
            return type_description

    async def add(
        self,
        type_description_id: int,
        si_modification: str,
        si_type: str,
        si_verification_date: datetime.date,
    ) -> Verification:
        async with self.session_factory() as session:
            type_description = await session.get(Verification, type_description_id)
            verification = Verification(
                type_description_id=type_description,
                si_modification=si_modification,
                si_type=si_type,
                si_verification_date=si_verification_date,
            )
            session.add(verification)

            await session.commit()
            await session.refresh(verification)
            return verification


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class VerificationNotFoundError(NotFoundError):
    entity_name: str = "Verification"
