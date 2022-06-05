from __future__ import annotations

import uuid

from sqlalchemy import Column, Date, Float, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.db import Base


class TypeDescription(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gos_number = Column(String)
    si_name = Column(String)
    si_unit_of_measurement = Column(String)
    si_measurement_error = Column(Float)
    si_measurement_error_type = Column(String)
    si_purpose = Column(String)
    si_approval_date = Column(Date)
    si_producer = Column(String)
    si_producer_country = Column(String)
    file_name = Column(String)
    # application_areas = relationship("ApplicationArea", secondary=association_table)

    __tablename__ = "type_description"
    __table_args__ = {'schema': 'measurement-data'}
