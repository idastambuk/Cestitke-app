# -*- coding: utf-8 -*-

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models.util import basic_validation
from ..models.meta import Session
from ..models.user import User

import logging

log = logging.getLogger(__name__)

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

REGISTER_KEYS =['first_name', 'last_name', 'email', 'password']

@view_config(route_name='register', renderer='cestitke:templates/registration.jinja2')
def register(request):
    register_url= request.route_url('register')
    referrer = '/' if request.url==register_url else request.url
    came_from = request.params.get('came_from', referrer)
    message= ''

    if not 'register.submit' in request.params:
        return dict(
            url=request.application_url + '/login',
            came_from=came_from
        )
    message, valid = check_parameters_valid(request.params)
    if not valid:
        return dict(
            register_error_message=message
        )
    elif not is_first_with_email(request.params['email']):
        return dict(
            register_error_mesasge="Korisnik s danim emailom ne postoji!"
        )
    store_user(
        request.params['first_name'], request.params['last_name'],
        request.params['email'], request.params['password']
    )
    process_login(request) #prijava korisnika nakon registracije
    return HTTPFound(location=came_from)

def is_first_with_email(email):
    user= Session.query(User).filter(User.email==email).first()
    if user:
        return False
    return True

def check_parameters_valid(params):
    params_keys = params.keys()
    errors =''
    valid = False

    for field_key in REGISTER_KEYS:
        if not field_key in params_keys:
            errors=u'Neki od parametara potrebnih za registraciju nisu proslijeđeni'
            return(errors, valid)

    if not basic_validation.validate_name(params['first_name']):
        errors = "{0}.{1}". format(errors, 'Ime nije u dobrom formatu')
    if not basic_validation.validate_name(params['last_name']):
        errors = "{0}.{1}". format(errors, 'Prezime nije u dobrom formatu')
    if not basic_validation.validate_email(params['email']):
        errors = "{0}.{1}". format(errors, 'Email nije u dobrom formatu')
    if not basic_validation.validate_password(params['password']):
        errors = "{0}.{1}". format(errors, 'Lozinka mora biti dulja od 3 znaka')
    if not errors:
        valid = True
    if errors.startswith('.'):
        errors= errors[1:]
        errors ='{0}!'. format(errors)
    return (errors,valid)


def store_user(first_name, last_name, email, password):
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(password)
    Session.add(user)
    Session.flush()
    log.info('Korisnik je dodan u bazu')
        
@view_config(route_name="login", renderer="cestitke:templates/login.jinja2")
def login(request):
    login_url= request.route_url("login")
    referrer = "/" if request.url == login_url else request.url
    came_from = request.params.get("came_from", referrer)
    message, email, password = "", "", ""
    if not "login.submit" in request.params:
        return dict(
            login_error_message=message,
            url=request.application_url + "/login",
            came_from=came_from
        )
    if not "email" in request.params or not "password" in request.params:
        message="Nedostaje lozinka ili email"
        return dict(
            login_error_message=message,
            url=request.application_url + "/login",
            came_from=came_from
        )
    success = process_login(request)
    if success:
        return HTTPFound(location=came_from)
    message = "Prijava neuspješna, pokušajte ponovno."
    return dict(
        login_error_message=message,
        url=request.application_url + "/login",
        came_from=came_from
    )

def process_login(request):
    email = request.params["email"]
    password = request.params["password"]
    user = Session.query(User).filter(User.email==email).first()
    if not user:
        return False
    if not user.check_password(password):
        return False
    request.session["user"] = {
        "user_name": user.first_name,
        "user_id": user.id,
        "user_email": user.email
    }
    return True

@view_config(route_name='logout', renderer='cestitke:templates/home.jinja2')
def logout(request):
    del request.session['user']
    return HTTPFound(location=request.resource_url(request.context))