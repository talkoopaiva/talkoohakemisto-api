"""Create `municipality` table

Revision ID: 3228d3c17da3
Revises: None
Create Date: 2014-02-08 15:22:58.071793

"""

# revision identifiers, used by Alembic.
revision = '3228d3c17da3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'municipality',
        sa.Column('code', sa.Integer, autoincrement=False, primary_key=True),
        sa.Column('name', sa.Unicode(20), nullable=False),
    )


def downgrade():
    op.drop_table('municipality')
