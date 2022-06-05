import uuid

from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class Verification(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_description_id = Column(UUID(as_uuid=True), ForeignKey("measurement-data.type_description.id"))
    si_modification = Column(String)
    si_type = Column(String)
    si_verification_date = Column(Date)
    si_verification_valid_until_date = Column(Date)

    __tablename__ = "verification"
    __table_args__ = {'schema': 'measurement-data'}
