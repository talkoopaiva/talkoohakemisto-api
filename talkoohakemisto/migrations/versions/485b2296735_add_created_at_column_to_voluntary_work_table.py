"""Add `created_at` column to `voluntary_work` table

Revision ID: 485b2296735
Revises: 63875fc6ebe
Create Date: 2014-02-09 21:38:45.394011

"""

# revision identifiers, used by Alembic.
revision = '485b2296735'
down_revision = '63875fc6ebe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'voluntary_work',
        sa.Column('created_at', sa.DateTime())
    )
    op.execute('UPDATE voluntary_work SET created_at = NOW()')
    op.alter_column('voluntary_work', 'created_at', nullable=False)


def downgrade():
    op.drop_column('voluntary_work', 'created_at')
