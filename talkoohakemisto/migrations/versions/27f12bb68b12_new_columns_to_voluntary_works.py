"""new columns to voluntary_works

Revision ID: 27f12bb68b12
Revises: 1ef4e5f61dac
Create Date: 2014-03-08 16:36:45.351031

"""

# revision identifiers, used by Alembic.
revision = '27f12bb68b12'
down_revision = '1ef4e5f61dac'

from alembic import op
import sqlalchemy as sa



def upgrade():
    op.add_column('voluntary_work', sa.Column('url', sa.Unicode(100), nullable=True))
    op.add_column('voluntary_work', sa.Column('hashtag', sa.Unicode(100), nullable=True))
    op.add_column('voluntary_work', sa.Column('location', sa.Unicode(100), nullable=True))
    op.add_column('voluntary_work', sa.Column('time', sa.Unicode(100), nullable=True))
    op.add_column('voluntary_work', sa.Column('goal', sa.Unicode(100), nullable=True))
    op.add_column('voluntary_work', sa.Column('contact_phone', sa.Unicode(100), nullable=True))
    op.add_column('voluntary_work', sa.Column('organization', sa.Unicode(100), nullable=True))
    pass


def downgrade():

    op.drop_column('voluntary_work', 'url')
    op.drop_column('voluntary_work', 'hashtag')
    op.drop_column('voluntary_work', 'location')
    op.drop_column('voluntary_work', 'time')
    op.drop_column('voluntary_work', 'goal')
    op.drop_column('voluntary_work', 'contact_phone')
    op.drop_column('voluntary_work', 'organization')
    pass
