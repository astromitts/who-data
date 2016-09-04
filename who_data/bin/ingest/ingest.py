import sys
import transaction
from copy import deepcopy
from who_data.lib.countries import (
    Countries,
    CountryAlias,
    sanitize_country_name
)
from who_data.bin.ingest.lib.who_file_parser import WHOFileParser
from who_data.bin.ingest import ABSOLUTE_FILE_PATH, primary_entity_file_map
from who_data.models.who import Country, WHODisease, WHODiseaseReport
from who_data.lib.urlizer import urlize


def main(ini_file):
    from who_data.models.base import Base, DBSession, set_engine
    set_engine(ini_file, Base, DBSession)
    for entity_key, entity_data in primary_entity_file_map.items():
        file_path = ABSOLUTE_FILE_PATH + entity_data['file']
        parsed_file = WHOFileParser(entity_key, file_path)
        parsed_file.parse()
        transaction.begin()
        who_disease = WHODisease.upsert(
            id=entity_key,
            name=entity_data['name'],
            info_link=entity_data['information-link'],
        )
        disease_id = deepcopy(who_disease.id)
        transaction.commit()

        for row in parsed_file.data:
            safe_country_name = sanitize_country_name(row['country'])
            py_country = Countries[safe_country_name]
            alias = CountryAlias.get(py_country.name)
            transaction.begin()
            country = Country().upsert(
                id=py_country.alpha2,
                name=py_country.name,
                url_name=urlize(py_country.name),
                alias=alias
            )
            country_id = deepcopy(country.id)
            transaction.commit()

            transaction.begin()
            for year, report_count in row['reports_by_year'].items():

                WHODiseaseReport.upsert(
                    country_id=country_id,
                    disease_id=disease_id,
                    year=year,
                    report_count=report_count,
                )
            transaction.commit()


if __name__ == "__main__":
    ini_file = sys.argv[1]
    sys.exit(main(ini_file))
