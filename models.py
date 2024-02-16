from flask_sqlalchemy import SQLAlchemy
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(100)) 
    instagram = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    properties = db.relationship('Property', backref='agent', lazy=True)
    rent_properties = db.relationship('RentProperty', backref='agent', lazy=True)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    area = db.Column(db.Float)
    beds = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    garage = db.Column(db.Integer)
    property_type = db.Column(db.String(50))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    images = db.relationship('PropertyImage', backref='property', lazy=True)

class PropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    
    
class RentProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    area = db.Column(db.Float)
    beds = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    garage = db.Column(db.Integer)
    property_type = db.Column(db.String(50))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    images = db.relationship('RentPropertyImage', backref='rent_property', lazy=True)

class RentPropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rent_property_id = db.Column(db.Integer, db.ForeignKey('rent_property.id'), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)

