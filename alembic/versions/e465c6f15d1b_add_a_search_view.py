"""add a search view

Revision ID: e465c6f15d1b
Revises: 640180a77a25
Create Date: 2016-09-06 20:02:50.663766

"""

# revision identifiers, used by Alembic.
revision = 'e465c6f15d1b'
down_revision = '640180a77a25'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.execute(
        "create view datastore.v_reports_search as "
        "select "
        "country.id as country_id, "
        "country.name as country_name, "
        "country.url_name as country_url_name, "
        "disease.id as disease_id, "
        "disease.name as disease_name, "
        "disease_report.year,  "
        "disease_report.report_count as count "
        "from datastore.disease_report "
        "join datastore.country on disease_report.country_id = country.id "
        "join datastore.disease on disease_report.disease_id = disease.id; "
    )


def downgrade():
    op.execute("drop view datastore.v_reports_search")
