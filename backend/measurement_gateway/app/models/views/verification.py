from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi_utils.api_model import APIModel
from pydantic.datetime_parse import date


class VerificationView(APIModel):
    id: UUID
    type_description_id: Optional[UUID]
    si_modification: Optional[str]
    si_type: Optional[str]
    si_verification_date: Optional[date]


class VerificationForm(APIModel):
    type_description_id: Optional[UUID]
    si_modification: Optional[str]
    si_type: Optional[str]
    si_verification_date: Optional[date]
