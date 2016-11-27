from sqlalchemy import Column, Integer, Unicode, Boolean
from .meta import Base
import bcrypt

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    first_name = Column(Unicode(255), nullable = False)
    last_name = Column(Unicode(255), nullable = False)
    email = Column(Unicode(255), nullable = False, unique = True)
    password_hash = Column(Unicode(128), nullable = True)
    security_token = Column(Unicode(128), nullable = True, unique = True)
    deleted = Column(Boolean, nullable = True, default = False)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash. decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False





