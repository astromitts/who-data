import sys
from bin.file_map import primary_entity_file_map
from lib.who_file_parser import WHOFileParser
from __init__ import ABSOLUTE_FILE_PATH


def main():
    for entity_key, file_name in primary_entity_file_map.items():
        file_path = ABSOLUTE_FILE_PATH + file_name
        parsed_file = WHOFileParser(entity_key, file_path)


if __name__ == "__main__":
    sys.exit(main())
