from sqlalchemy import Column, Integer, Unicode, Boolean, ForeignKey, UnicodeText, DateTime
from sqlalchemy.orm import relationship
from .meta import Base

from datetime import datetime

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key = True)
    path = Column(Unicode(255), nullable = False)
    deleted = Column(Boolean, nullable = False, default = False)

class Frame(Base):
    __tablename__ = 'frame'
    id = Column(Integer, primary_key = True)
    path = Column(Unicode(255), nullable = False)
    name = Column(Unicode(255), nullable = False)
    deleted = Column(Boolean, nullable = False, default = False)


class Ecard(Base):
    __tablename__ = 'ecard'
    id = Column(Integer, primary_key = True)
    title = Column(Unicode(255), nullable = False)
    message = Column(UnicodeText(), nullable = True)
    public = Column(Boolean, nullable = False, default = False)
    last_change_date = Column(DateTime, nullable = False, default = datetime.utcnow())
    user_id = Column(ForeignKey('user.id'), nullable = False)
    image_id = Column(ForeignKey('image.id'), nullable = False)
    frame_id = Column(ForeignKey('frame.id'), nullable = False)
    deleted = Column(Boolean, nullable = False, default = False)

    user = relationship('User', backref = 'ecards')
    frame = relationship('Frame', backref = 'ecards')
    image = relationship('Image', backref = 'ecards')