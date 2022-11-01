from app import db

class Bike(db.Model): #inheriting from db model - don't have to do a constructor def below
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # putting data type and Primary key syntax 
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    size = db.Column(db.Integer)
    type = db.Column(db.String) # want this model to be a table in our db by letting migrate tool know it exists

# this is how we say what we want our table to look like

