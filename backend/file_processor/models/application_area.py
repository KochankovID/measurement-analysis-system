import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base
from models.associated_table import association_table


class ApplicationArea(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_descriptions = relationship("TypeDescription", secondary=association_table)
    application_area_name = Column(String)

    __tablename__ = "application_area"
    __table_args__ = {'schema': 'measurement-data'}
