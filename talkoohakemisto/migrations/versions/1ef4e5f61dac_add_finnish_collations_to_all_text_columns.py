"""Add Finnish collations to all text columns

Revision ID: 1ef4e5f61dac
Revises: 485b2296735
Create Date: 2014-02-09 21:51:35.842781

"""

# revision identifiers, used by Alembic.
revision = '1ef4e5f61dac'
down_revision = '485b2296735'

from alembic import op


def upgrade():
    op.execute(
        '''
        ALTER TABLE municipality
        ALTER COLUMN name
        TYPE varchar(20)
        COLLATE "fi_FI.utf8"
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work_type
        ALTER COLUMN name
        TYPE varchar(50)
        COLLATE "fi_FI.utf8"
        '''
    )

    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN name
        TYPE varchar(100)
        COLLATE "fi_FI.utf8"
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN organizer
        TYPE varchar(100)
        COLLATE "fi_FI.utf8"
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN description
        TYPE text
        COLLATE "fi_FI.utf8"
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN street_address
        TYPE varchar(100)
        COLLATE "fi_FI.utf8"
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN contact_email
        TYPE varchar(100)
        COLLATE "fi_FI.utf8"
        '''
    )


def downgrade():
    op.execute(
        '''
        ALTER TABLE municipality
        ALTER COLUMN name
        TYPE varchar(20)
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work_type
        ALTER COLUMN name
        TYPE varchar(50)
        '''
    )

    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN name
        TYPE varchar(100)
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN organizer
        TYPE varchar(100)
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN description
        TYPE text
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN street_address
        TYPE varchar(100)
        '''
    )
    op.execute(
        '''
        ALTER TABLE voluntary_work
        ALTER_COLUMN contact_email
        TYPE varchar(100)
        '''
    )
