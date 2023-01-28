from flask import Flask,render_template,request,url_for,redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'CierrateSesamos'
db=SQLAlchemy(app)
db.init_app(app)
# db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))

# class Todo(db.Model):
#     id= db.Column(db.Integer, primary_key = True)
#     description = db.Column(db.String (180))
#     is_completed = db.Column(db.Boolean)
#     user_id =db.Column(db.Integer, db.ForeignKey('user.id'))




class RegisterForm(FlaskForm):
    username = StringField()
    email= StringField()
    password = PasswordField()
    submit = SubmitField('Register')

# @app.before_first_request
# def create_tables():
   

@app.route('/')
def home():
    # todos = Todo.query(user_id = id)
    return 'Hello world'

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        # aca
        db.session.commit()
        print('comitee la puta madre')
        # return redirect(url_for('login'))
        return redirect(url_for('register'))
    return render_template('register.html',form=form)

    

if __name__ == '__main__':

    app.run(debug=True)
    