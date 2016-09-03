import pycountry

# these countries are known variations from WHO compared to the
# pycountry library, so they need to be mapped
known_name_mapping = {
    'Bolivia, Plurinational State of': 'Bolivia (Plurinational State of)',
    'Côte d\'Ivoire': 'Cote d\'Ivoire',
    'Cape Verde': 'Cabo Verde',
    'Korea, Democratic People\'s Republic of':
        'Democratic People\'s Republic of Korea',
    'Korea, Republic of': 'republic of korea',
    'Congo, The Democratic Republic of the':
        'Democratic Republic of the Congo',
    'Moldova, Republic of': 'republic of moldova',
    'Macedonia, Republic of': 'the former yugoslav republic of macedonia',
    'United Kingdom':
        'united kingdom of great britain and northern ireland',
    'Tanzania, United Republic of': 'united republic of tanzania',
    'United States': 'united states of america',
}

def sanitize_country_name(name):
    return name.replace('(', '').replace(')', '').replace(',', '').lower()

Countries = {}
for country in pycountry.countries:
    Countries[sanitize_country_name(country.name)] = country
    if country.name in known_name_mapping:
        Countries[
            sanitize_country_name(known_name_mapping[country.name])
        ] = country
