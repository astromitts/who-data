def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.route_prefix = config.get_settings().get('url_prefix')

    routes = [
        ('home', ''),
        ('api_v1_ping', '/api/{api_version}/ping'),
        ('api_v1_country_search', '/api/{api_version}/countries'),
        ('api_v1_country_resource', '/api/{api_version}/countries/{url_name}'),
        ('api_v1_disease_landing', '/api/{api_version}/diseases'),
        ('api_v1_disease_resource', '/api/{api_version}/diseases/{url_name}'),
        ('api_v1_disease_search',
            '/api/{api_version}/diseases/{url_name}/search'),
        ('api_v1_disease_year_resource',
            '/api/{api_version}/diseases/{url_name}/{year}'),
    ]

    config.add_route
    for route in routes:
        config.add_route(route[0], route[1])
