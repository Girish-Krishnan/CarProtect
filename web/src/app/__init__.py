from pyramid.config import Configurator

from . import routes


def create_app():
    """Create and configure the Pyramid WSGI application."""
    config = Configurator()
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_route('get_home', '/')
    config.add_view(routes.get_home, route_name='get_home')

    config.add_route('unlock', '/unlock/{username}/{password}/')
    config.add_view(routes.get_unlock, route_name='unlock', renderer='json')

    config.add_route(
        'send_data',
        '/send_data/{username}/{password}/{pir}/{vib}/{ax}/{ay}/{az}/{lat}/{long}/'
    )
    config.add_view(routes.send_data, route_name='send_data', renderer='json')

    config.add_route('stream_data', '/stream_data/{username}/{password}/')
    config.add_view(routes.stream_data, route_name='stream_data', renderer='json')

    config.add_route('store', '/store_mp3_view/')
    config.add_view(routes.store_image, route_name='store')

    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    return config.make_wsgi_app()
