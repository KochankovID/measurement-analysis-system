from __future__ import annotations

from sqlalchemy import Column, Float, Identity, Integer, String
from sqlalchemy.orm import relationship

from app.db.db import Base


class TypeDescription(Base):
    __tablename__ = "type_description.puml"
    id = Column(Integer, Identity(), primary_key=True)
    gos_number = Column(String)
    si_name = Column(String)
    si_unit_of_measurement = Column(String)
    si_measurement_error = Column(Float)
    file_name = Column(String)
