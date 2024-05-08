
from db import db, login_manager
from flask_login import UserMixin
from apps.authentication.util import hash_pass
import uuid

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.relationship('AgentImage', backref='agent')
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(100)) 
    instagram = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    properties = db.relationship('Property', backref='agent', lazy=True, uselist=False, cascade='all, delete-orphan')

class AgentImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.String(200), nullable=False)
    property_status = db.Column(db.String(10), nullable=False)
    area = db.Column(db.Float)
    bathroom = db.Column(db.Integer)
    garage = db.Column(db.Integer)
    property_type = db.Column(db.String(50))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    images = db.relationship('PropertyImage', backref='property', lazy=True, uselist=True, cascade='all, delete-orphan')

class PropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)

class Visitor(db.Model):
    __tablename__ = 'visitors'
    
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    visit_count = db.Column(db.Integer, default=1)

    def __init__(self, **kwargs):
        super(Visitor, self).__init__(**kwargs)
        if not self.visitor_id:
            self.visitor_id = str(uuid.uuid4())

    def __repr__(self):
        return f'<Visitor {self.visitor_id}>'
    
    
class Users(db.Model, UserMixin):
    
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
