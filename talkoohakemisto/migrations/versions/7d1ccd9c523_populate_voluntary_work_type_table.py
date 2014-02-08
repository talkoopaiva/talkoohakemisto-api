# -*- coding: utf-8 -*-
"""Populate `voluntary_work_type` table

Revision ID: 7d1ccd9c523
Revises: 597b5983e01c
Create Date: 2014-02-08 17:21:59.398083

"""

# revision identifiers, used by Alembic.
revision = '7d1ccd9c523'
down_revision = '597b5983e01c'

from alembic import op


TYPES = [
    (u'Kohtaaminen',),
    (u'Korjaamo',),
    (u'Kunnostus',),
    (u'Siivous',),
    (u'Taitopaja',),
    (u'Treenit',),
    (u'Työpaja',),
]


def upgrade():
    conn = op.get_bind()
    conn.execute(
        'INSERT INTO voluntary_work_type (name) VALUES (%s)',
        *TYPES
    )


def downgrade():
    op.execute('DELETE FROM voluntary_work_type')
