from pyramid.config import Configurator
from zope.sqlalchemy.datamanager import ZopeTransactionExtension
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from cestitke.models.meta import Session, Base
from sqlalchemy import engine_from_config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy(
        'radionica', callback=None, hashalg='sha512')
    session_factory = SignedCookieSessionFactory('radionica')
    config = Configurator(
        settings = settings, authentication_policy=authn_policy,
        authorization_policy = ACLAuthorizationPolicy(),
        session_factory=session_factory)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    engine= engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    return config.make_wsgi_app()
