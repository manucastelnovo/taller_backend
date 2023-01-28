from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'chupetess'
db = SQLAlchemy(app)

class RegisterForm(FlaskForm):
    username = StringField()
    email= EmailField()
    password = PasswordField()
    submit = SubmitField('Register')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    
    def __repr__(self):
        return '<User %r>' % self.username
    


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(180))
    is_completed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<todo %r>' % self.todo


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
        return redirect(url_for('register'))
    return render_template('index.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
