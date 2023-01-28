from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    
    def __repr__(self):
        return '<User %r>' % self.username
    


# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(180))
#     is_completed = db.Column(db.Boolean)
#     user_id = db.Column(db.Integer, db.ForeingKey('user.id'))
    
#     def __repr__(self):
#         return '<todo %r>' % self.todo


@app.route('/', methods=['GET'])
def home():
    user = User.query.all()
    return 'iuesaasheasaeaeassaeehjaseaesaeassa'


if __name__ == '__main__':
    app.run(debug=True)
