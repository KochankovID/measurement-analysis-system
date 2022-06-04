from concurrent.futures import Future
from typing import Iterator, List

from app.models.sqalchemy.type_description import TypeDescription
from app.repositories.type_description_repository import TypeDescriptionRepository


class TypeDescriptionService:
    def __init__(self, type_desc_repository: TypeDescriptionRepository) -> None:
        self._repository: TypeDescriptionRepository = type_desc_repository

    async def get_type_descriptions(self) -> List[TypeDescription]:
        return await self._repository.get_all()

    async def get_type_description_by_id(self, type_description_id: int) -> TypeDescription:
        return await self._repository.get_by_id(type_description_id)

    async def create_type_description(
        self,
        gos_number: str,
        si_name: str,
        si_unit_of_measurement: str,
        si_measurement_error: float,
        file_name: str,
    ) -> TypeDescription:
        return await self._repository.add(
            gos_number=gos_number,
            si_name=si_name,
            si_unit_of_measurement=si_unit_of_measurement,
            si_measurement_error=si_measurement_error,
            file_name=file_name,
        )
