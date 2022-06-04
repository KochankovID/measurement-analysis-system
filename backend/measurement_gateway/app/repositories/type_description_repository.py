from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sqalchemy.type_description import TypeDescription


class TypeDescriptionRepository:
    def __init__(
            self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.session_factory = session_factory

    async def get_all(self) -> List[TypeDescription]:
        async with self.session_factory() as session:
            type_descriptions = await session.execute(
                select(TypeDescription)
            )
            return type_descriptions.scalars().all()

    async def get_by_id(self, type_description_id: int) -> TypeDescription:
        async with self.session_factory() as session:
            type_description = await session.get(TypeDescription, type_description_id)
            if not type_description:
                raise TypeDescriptionNotFoundError(type_description)
            return type_description

    async def add(
            self,
            gos_number: str,
            si_name: str,
            si_unit_of_measurement: str,
            si_measurement_error: float,
            file_name: str,
    ) -> TypeDescription:
        async with self.session_factory() as session:
            type_description = TypeDescription(
                gos_number=gos_number,
                si_name=si_name,
                si_unit_of_measurement=si_unit_of_measurement,
                si_measurement_error=si_measurement_error,
                file_name=file_name,
            )
            session.add(type_description)

            await session.commit()
            await session.refresh(type_description)
            return type_description


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class TypeDescriptionNotFoundError(NotFoundError):
    entity_name: str = "TypeDescription"
