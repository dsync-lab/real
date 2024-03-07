
from db import db


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
    
    

