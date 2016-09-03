def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    # empty search result page, used for testing
    config.add_route('search_ping', '/search/ping')

    # Country search end point
    config.add_route('search_country', '/search/countries')
    config.add_route('search_country', '/search/countries/{country-url-name}')
