from collections import OrderedDict

ABSOLUTE_FILE_PATH = 'who_data/bin/data/who-source-files/'

primary_entity_file_map = OrderedDict([
    ('rabies', {
        'file': 'rabies.csv',
        'name': 'Rabies',
        'information-link': 'http://www.who.int/rabies/en/',
    }),
    ('river-blindness', {
        'file': 'onchocerciasis-river-blindeness.csv',
        'name': 'Onchocerciasis (river blindeness)',
        'information-link': 'http://www.who.int/topics/onchocerciasis/en/',
    }),
    ('leprosy', {
        'file': 'leprosy.csv',
        'name': 'Leprosy',
        'information-link': 'http://www.who.int/lep/en/',
    }),
    ('sleeping-sickness', {
        'file': 'humanafrican-trypanosomiasis-sleeping-sickness.csv',
        'name': 'Humanafrican Trypanosomiasis (sleeping sickness)',
        'information-link': 'http://www.who.int/trypanosomiasis_african/en/',
    }),
    ('guinea-worm', {
        'file': 'dracunculiasis-guinea-worm.csv',
        'name': 'Dracunculiasis (guinea worm)',
        'information-link': 'http://www.who.int/dracunculiasis/en/',
    }),
    ('buruli-ulcer', {
        'file': 'buruli-ulcer.csv',
        'name': 'Buruli Ulcer',
        'information-link': (
            'http://www.who.int/mediacentre/factsheets/fs199/en/'
        ),
    })
])
