from sqlalchemy import Column, Integer, String, column
from sqlalchemy.dialects import postgresql

from db import Base


class RegexSettings(Base):
    id = Column(Integer, primary_key=True)
    type_description = Column(postgresql.ARRAY(String))
    meaning = Column(postgresql.ARRAY(String))
    measurement_unit = Column(postgresql.ARRAY(String))
    description = Column(postgresql.ARRAY(String))

    __tablename__ = "regex_settings"
    __table_args__ = {'schema': 'measurement-admin'}
