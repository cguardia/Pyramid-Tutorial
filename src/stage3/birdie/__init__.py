from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from birdie.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    authentication_policy = AuthTktAuthenticationPolicy('b1rd13')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory='birdie.models.RootFactory',
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          settings=settings)
    config.add_static_view('static', 'birdie:static')
    config.add_route('home', '/')
    config.add_route('join', '/join')
    config.add_route('logout', '/logout')
    config.add_route('follow', '/follow/{userid}')
    config.add_route('unfollow', '/unfollow/{userid}')
    config.add_route('users', '/{userid}')
    config.scan('birdie')
    return config.make_wsgi_app()

