from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ..models.meta import Session
from ..models.ecard import Frame, Ecard, Image

from datetime import datetime

import os
import shutil
import uuid

ECARD_ACCESS = {"yes": True, "no": False}

@view_config(route_name='add', renderer='cestitke:templates/add.jinja2')
def add(request):
    try:
        user_id = request.session['user']['user_id']
    except:
        return {"add_error_message": "Prijavite se da biste dodali cestitku."}
    if 'cardadd.submit' not in request.params:
        return {"add_error_message": ""}
    title, message, frame, img, private, err = get_params(request)
    if err:
        return {"add_error_message": err}
    try:
        create_ecard(user_id, title, message, frame, img, private)
    except:
        return {"add_error_message": "Spremanje cestitke nije uspjelo."}
    return HTTPFound(location='/my')

@view_config(route_name='ecardedit', renderer='cestitke:templates/edit.jinja2')
def ecardedit(request):
    ecard_id = request.matchdict.get('id', None)
    if not ecard_id:
        return HTTPNotFound()
    ecard = Session.query(Ecard).filter(Ecard.id == ecard_id).first()
    if not ecard:
        return HTTPNotFound()
    if not request.method == 'POST':
        return {"ecard":ecard, "edit_error_message":""}
    title, message, frame, img, private, err = get_params(request)
    if err:
        return{"edit_error_message": err, "ecard": ecard}
    ecard.title = title if title else ecard.title
    ecard.message= message if message else ecard.message
    ecard.frame = Session.query(Frame).filter(Frame.name == frame).first() if frame else ecard.frame
    try:
        new_image = create_image(img)
    except:
        print "Slika nije spremljena."
    if new_image is not None:
        ecard.img = new_image
    ecard.public = not ECARD_ACCESS[private]
    ecard.last_change_date = datetime.utcnow()
    return HTTPFound(location='/my')




def get_params(request):
    try:
        title = request.POST['title']
        message = request.POST['message']
        frame = request.POST['frame']
        img = request.POST['img']
    except:
        return None, None, None, None, None, "Neki parametri nedostaju."
    try:
        private = request.POST['private_card']
    except:
        private = 'no'
    return (title, message, frame, img, private, "")

def create_ecard(user_id, title, message, frame, img, private, deleted=False):
    image = create_image(img) if img is not None else None
    ecard = Ecard()
    print frame
    print Session.query(Frame).all()
    frame_obj = Session.query(Frame).filter(Frame.name == frame).first()
    ecard.title = unicode(title)
    ecard.message = unicode(message)
    ecard.deleted = deleted
    ecard.public = not ECARD_ACCESS[private]
    ecard.user_id = user_id
    # nedostajala je dodjela ID-a okvira koji je potreban za kreiranje cestitke
    ecard.frame_id = frame_obj.id
    ecard.last_change_date = datetime.utcnow()
    if image is not None:
        ecard.image_id = image.id
    Session.add(ecard)
    Session.flush()

def create_image(img):
    try:
        img_file = img.file
        img_filename = img.filename
    except:
        return None
    uuid_prefix = uuid.uuid4()
    store_path = os.path.join("../static/uploaded", 
        "{0}{1}".format(uuid_prefix, img_filename))
    store_path_abs = os.path.abspath(os.path.join(
        "cestitke/static/uploaded", 
        "{0}{1}".format(uuid_prefix, img_filename)
    ))
    img_file.seek(0)
    with open(store_path_abs, 'wb') as output_file:
        shutil.copyfileobj(img_file, output_file)
    image = Image()
    image.path = store_path
    image.deleted = False
    Session.add(image)
    Session.flush()
    return image
    
@view_config(route_name='my', renderer = 'cestitke:templates/home.jinja2')
def my(request):
    try:
        logged_user_id = request.session['user']['user_id']
    except:
        return {my_ecards: []}
    my_ecards = Session.query(Ecard).filter(Ecard.user_id == logged_user_id, Ecard.deleted == False).all()

    return {"ecards" : my_ecards}


@view_config(route_name='ecarddelete')
def ecarddelete(request):
    ecard_id=request.matchdict.get('id', None)
    if not ecard_id:
        return HTTPNotFound()
    
    ecard = Session.query(Ecard).filter(Ecard.id == ecard_id).first()

    if not ecard:
        return HTTPFound()
    
    ecard.deleted=True
    ecard.last_change_date = datetime.utcnow()
    return HTTPFound('/my')

@view_config(route_name='ecard', renderer='cestitke:templates/home.jinja2')
def ecard(request):
    ecard_id=request.matchdict.get("id", None)
    if not ecard_id:
        return HTTPNotFound()
    ecard = Session.query(Ecard).filter(Ecard.id == ecard_id).first()

    if not ecard:
        return HTTPNotFound()
    
    return{'ecards': [ecard]}






