from typing import Optional
from uuid import UUID

from fastapi_utils.api_model import APIModel


class TypeDescriptionView(APIModel):
    id: UUID
    gos_number: Optional[str]
    si_name: Optional[str]
    si_unit_of_measurement: Optional[str]
    si_measurement_error: Optional[float]
    file_name: Optional[str]


class TypeDescriptionForm(APIModel):
    gos_number: Optional[str]
    si_name: Optional[str]
    si_unit_of_measurement: Optional[str]
    si_measurement_error: Optional[float]
    file_name: Optional[str]
