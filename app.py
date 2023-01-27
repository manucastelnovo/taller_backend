from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask (__name__)
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String (180))
    is_completed = db.Column(db.Boolean)
    user_id =db.Column(db.Integer, db.ForeingKey('user.id'))

@app.route('/')
def home():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True)