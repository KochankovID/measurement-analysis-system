import uuid

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.db import Base
from app.models.sqalchemy.associated_table import association_table
from app.models.sqalchemy.type_description import TypeDescription


class ApplicationArea(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_descriptions = relationship("TypeDescription", secondary=association_table)
    application_area_name = Column(String)

    __tablename__ = "application_area"
    __table_args__ = {'schema': 'measurement-data'}
