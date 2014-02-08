"""Create `voluntary_work_type` table

Revision ID: 597b5983e01c
Revises: 2e20f23a8ffd
Create Date: 2014-02-08 17:14:35.812815

"""

# revision identifiers, used by Alembic.
revision = '597b5983e01c'
down_revision = '2e20f23a8ffd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'voluntary_work_type',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.Unicode(50), nullable=False),
    )


def downgrade():
    op.drop_table('voluntary_work_type')
