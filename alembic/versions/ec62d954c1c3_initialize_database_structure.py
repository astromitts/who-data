"""Initialize database structure

Revision ID: ec62d954c1c3
Revises:
Create Date: 2016-09-02 20:25:17.058257

"""

# revision identifiers, used by Alembic.
revision = 'ec62d954c1c3'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.execute('create schema if not exists datastore')

    op.create_table(
        'country',
        sa.Column('id', sa.Text, nullable=False),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('alias', postgresql.ARRAY(sa.String())),
        sa.PrimaryKeyConstraint('id', name='pk_country_id'),
        sa.UniqueConstraint('name', name='uq_country_name'),
        schema='datastore'
    )
    op.execute(
        'create index ix_country_name_lower on datastore.country(lower(name))'
    )
    op.execute(
        'create index ix_country_alias_lower on datastore.country '
        'using gin ("alias")'
    )
    op.create_table(
        'disease',
        sa.Column('id', sa.Text, nullable=False),
        sa.Column('name', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_disease_id'),
        sa.UniqueConstraint('name', name='uq_disease_name'),
        schema='datastore'
    )
    op.execute(
        'create index ix_disease_name on datastore.disease(name)'
    )

    op.create_table(
        'disease_report',
        sa.Column('id', sa.INTEGER, autoincrement=True, nullable=False),
        sa.Column('country_id', sa.Text, nullable=False),
        sa.Column('disease_id', sa.Text, nullable=False),
        sa.Column('year', sa.INTEGER, nullable=False),
        sa.Column('report_count', sa.INTEGER),
        sa.PrimaryKeyConstraint('id', name='pk_disease_report_id'),
        sa.UniqueConstraint(
            'year',
            'country_id',
            'disease_id',
            name='uq_disease_report_year_country_disease'
        ),
        sa.ForeignKeyConstraint(
            name='fk_disease_report_disease_id',
            columns=['disease_id'], refcolumns=['datastore.disease.id']
        ),
        sa.ForeignKeyConstraint(
            name='fk_disease_report_country_id',
            columns=['country_id'], refcolumns=['datastore.country.id']
        ),
        schema='datastore'
    )
    op.execute(
        'create index ix_disease_report_count on '
        'datastore.disease_report(report_count)'
    )


def downgrade():
    op.drop_table('disease_report', schema='datastore')
    op.drop_table('country', schema='datastore')
    op.drop_table('disease', schema='datastore')
    op.execute('drop schema datastore')
