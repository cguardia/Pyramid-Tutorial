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
    config.add_view('birdie.views.birdie_view',
                    route_name='home',
                    permission='view',
                    renderer='templates/birdie.pt')
    config.add_view('birdie.views.birdie_post',
                    route_name='home',
                    permission='view',
                    request_method='POST',
                    renderer='templates/birdie.pt')
    config.add_view('birdie.views.login_page',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    request_method='GET',
                    renderer='templates/login.pt')
    config.add_view('birdie.views.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    request_method='POST',
                    renderer='templates/login.pt')
    config.add_view('birdie.views.logout',
                    route_name='logout')
    config.add_view('birdie.views.join',
                    route_name='join',
                    request_method='POST',
                    renderer='templates/join.pt')
    config.add_view('birdie.views.join_page',
                    route_name='join',
                    request_method='GET',
                    renderer='templates/join.pt')
    return config.make_wsgi_app()

