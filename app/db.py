from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Earthquake(db.Model):
    __tablename__ = 'earthquakes'

    id = db.Column(db.String, primary_key=True)
    time = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    depth = db.Column(db.Float)
    mag = db.Column(db.Float)
    place = db.Column(db.String)
    type = db.Column(db.String)