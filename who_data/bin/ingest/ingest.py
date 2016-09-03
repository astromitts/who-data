import sys
import transaction
from who_data.bin.countries import Countries, sanitize_country_name
from who_data.bin.ingest.bin.file_map import primary_entity_file_map
from who_data.bin.ingest.lib.who_file_parser import WHOFileParser
from who_data.bin.ingest import ABSOLUTE_FILE_PATH
from who_data.models.who import Country


def main(ini_file):
    from who_data.models.base import Base, DBSession, set_engine
    set_engine(ini_file, Base, DBSession)
    for entity_key, file_name in primary_entity_file_map.items():
        file_path = ABSOLUTE_FILE_PATH + file_name
        parsed_file = WHOFileParser(entity_key, file_path)
        parsed_file.parse()
        for row in parsed_file.data:
            transaction.begin()
            safe_country_name = sanitize_country_name(row['country'])
            py_country = Countries[safe_country_name]
            country = Country().create_get_by_id(
                id=py_country.alpha2,
                name=py_country.name
            )
            transaction.commit()


if __name__ == "__main__":
    ini_file = sys.argv[1]
    sys.exit(main(ini_file))
