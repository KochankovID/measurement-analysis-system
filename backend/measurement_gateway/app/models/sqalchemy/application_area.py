from sqlalchemy import Column, ForeignKey, Identity, Integer, String

from app.db.db import Base


class ApplicationArea(Base):
    __tablename__ = "application_area"
    id = Column(Integer, Identity(), primary_key=True)
    type_description_id = Column(Integer, ForeignKey("type_description.id"))
    application_area_name = Column(String)
