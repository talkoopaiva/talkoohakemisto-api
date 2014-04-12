"""adjust goal and description size

Revision ID: 221e6ee3f6c9
Revises: 27f12bb68b12
Create Date: 2014-04-12 17:04:16.750942

"""

# revision identifiers, used by Alembic.
revision = '221e6ee3f6c9'
down_revision = '27f12bb68b12'

from alembic import op
import sqlalchemy as sa



def upgrade():
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER COLUMN description
        TYPE text
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER COLUMN goal
        TYPE text
        '''
    )
    pass


def downgrade():
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER COLUMN description
        TYPE varchar(100)
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER COLUMN goal
        TYPE varchar(100)
        '''
    )
    pass
