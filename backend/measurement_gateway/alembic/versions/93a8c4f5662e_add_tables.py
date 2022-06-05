"""Add tables

Revision ID: 93a8c4f5662e
Revises: 
Create Date: 2022-06-05 02:15:31.750539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '93a8c4f5662e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_area',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('application_area_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='measurement-data'
    )
    op.create_table('type_description',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('gos_number', sa.String(), nullable=True),
    sa.Column('si_name', sa.String(), nullable=True),
    sa.Column('si_unit_of_measurement', sa.String(), nullable=True),
    sa.Column('si_measurement_error', sa.Float(), nullable=True),
    sa.Column('si_measurement_error_type', sa.String(), nullable=True),
    sa.Column('si_purpose', sa.String(), nullable=True),
    sa.Column('si_approval_date', sa.Date(), nullable=True),
    sa.Column('si_producer', sa.String(), nullable=True),
    sa.Column('si_producer_country', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='measurement-data'
    )
    op.create_table('association',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('application_area', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('type_description', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['application_area'], ['measurement-data.application_area.id'], ),
    sa.ForeignKeyConstraint(['type_description'], ['measurement-data.type_description.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='measurement-data'
    )
    op.create_table('verification',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('type_description_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('si_modification', sa.String(), nullable=True),
    sa.Column('si_type', sa.String(), nullable=True),
    sa.Column('si_verification_date', sa.Date(), nullable=True),
    sa.Column('si_verification_valid_until_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['type_description_id'], ['measurement-data.type_description.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='measurement-data'
    )