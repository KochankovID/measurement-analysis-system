from sqlalchemy import Column, Date, ForeignKey, Identity, Integer, String

from app.db.db import Base


class Verification(Base):
    __tablename__ = "verification"
    id = Column(Integer, Identity(), primary_key=True)
    type_description_id = Column(Integer, ForeignKey("type_description.id"))
    si_modification = Column(String)
    si_type = Column(String)
    si_verification_date = Column(Date)
