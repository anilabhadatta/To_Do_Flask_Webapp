from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class notes(db.Model):
    __tablename__ = "notes"
 
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String())
 
    def __init__(self, notes):
        self.notes = notes