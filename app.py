from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'chupetess'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class RegisterForm(FlaskForm):
    username = StringField()
    email= EmailField()
    password = PasswordField()
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')



class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    
    def __repr__(self):
        return '<User %r>' % self.name
    


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(180))
    is_completed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<todo %r>' % self.todo


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        # aca
        db.session.commit()
        print('comitee la puta madre')
        # return redirect(url_for('login'))
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user:
            print("entre en el if")
            login_user(user)
            # return redirect(url_for('user'))
            return 'PUTOOOO'

        return '<h1>Invalid username or passord</h1>'

    return render_template('login.html', form=form)
    


if __name__ == '__main__':
    app.run(debug=True)
