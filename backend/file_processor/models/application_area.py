import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class ApplicationArea(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_description_id = Column(UUID, ForeignKey("measurement-data.type_description.id"))
    application_area_name = Column(String)

    __tablename__ = "application_area"
    __table_args__ = {'schema': 'measurement-data'}
