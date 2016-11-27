from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models.meta import Session
from ..models.ecard import Ecard



@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    ecards = Session.query(Ecard).filter(Ecard.deleted == False, Ecard.public == 1).order_by(Ecard.last_change_date.desc()).all()
    return {"ecards": ecards}





db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_cestitke_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
