import uuid

from sqlalchemy import Column, ForeignKey, Table

from app.db.db import Base
from sqlalchemy.dialects.postgresql import UUID

association_table = Table(
    "association",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("application_area", ForeignKey("measurement-data.application_area.id")),
    Column("type_description", ForeignKey("measurement-data.type_description.id")),
    schema="measurement-data"
)
