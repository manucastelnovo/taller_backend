from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
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
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        # aca
        db.session.commit()
        print('comitee la puta madre')
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
            hashed_pass = check_password_hash(user.password, form.password.data)
            if hashed_pass:
                login_user(user)
                # return redirect(url_for('user'))
                return redirect(url_for('todo'))

        return '<h1>Invalid username or passord</h1>'

    return render_template('login.html', form=form)

@app.route('/todo', methods=['POST','GET'])
@login_required
def todo():
    todos =Todo.query.filter_by(user_id=current_user.id)
    if request.method == 'POST':
        print(request.form['description'])
        todo = Todo(
            description=request.form['description'],
            is_completed=False,
            user_id=current_user.id
        )
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo'))
    
    return render_template('index.html', todos=todos)

@app.route('/update/<int:todo_id>')
@login_required
def update_todo(todo_id):
    todo_to_be_updated = Todo.query.filter_by(id=todo_id).first()
    todo_to_be_updated.is_completed = not todo_to_be_updated.is_completed
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo_to_be_deleted = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo_to_be_deleted)
    db.session.commit()
    return redirect(url_for('todo'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))
    


if __name__ == '__main__':
    app.run(debug=True)
