"""add info-link field to disease resource table

Revision ID: 640180a77a25
Revises: ec62d954c1c3
Create Date: 2016-09-04 10:36:30.283377

"""

# revision identifiers, used by Alembic.
revision = '640180a77a25'
down_revision = 'ec62d954c1c3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE datastore.disease ADD COLUMN info_link TEXT')


def downgrade():
    op.execute('ALTER TABLE datastore.disease DROP COLUMN info_link')
