"""Create `voluntary_work` table

Revision ID: 63875fc6ebe
Revises: 7d1ccd9c523
Create Date: 2014-02-09 13:49:24.946138

"""

# revision identifiers, used by Alembic.
revision = '63875fc6ebe'
down_revision = '7d1ccd9c523'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'voluntary_work',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(length=100), nullable=False),
        sa.Column('organizer', sa.Unicode(length=100), nullable=False),
        sa.Column('description', sa.UnicodeText(), nullable=False),
        sa.Column('street_address', sa.Unicode(length=100), nullable=False),
        sa.Column('contact_email', sa.Unicode(length=100), nullable=False),
        sa.Column('type_id', sa.Integer(), nullable=False),
        sa.Column('municipality_code', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['municipality_code'], ['municipality.code']),
        sa.ForeignKeyConstraint(['type_id'], ['voluntary_work_type.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('voluntary_work')
