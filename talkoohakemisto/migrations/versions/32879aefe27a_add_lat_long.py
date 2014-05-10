"""add lat & long

Revision ID: 32879aefe27a
Revises: 221e6ee3f6c9
Create Date: 2014-05-06 19:18:43.918883

"""

# revision identifiers, used by Alembic.
revision = '32879aefe27a'
down_revision = '221e6ee3f6c9'

from alembic import op
import sqlalchemy as sa



def upgrade():
    op.add_column('voluntary_work', sa.Column('lat', sa.Float, nullable=True))
    op.add_column('voluntary_work', sa.Column('lng', sa.Float, nullable=True))
    pass


def downgrade():
    op.drop_column('voluntary_work', 'lat')
    op.drop_column('voluntary_work', 'lng')
    pass
