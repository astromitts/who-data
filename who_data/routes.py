def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.route_prefix = 'who-data'

    routes = [
        ('api_v1_ping', '/api/{api_version}/ping'),
        ('api_v1_country_landing', '/api/{api_version}/countries'),
        ('api_v1_country', '/api/{api_version}/countries/{country_url_name}'),
    ]

    config.add_route
    for route in routes:
        config.add_route(route[0], route[1])
