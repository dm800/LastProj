from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.loginform import LoginForm
from data.registerform import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param["id"] = current_user.id if current_user.is_authenticated else 0
    param["avatar"] = current_user.avatar if current_user.is_authenticated else "avatars/id0.png"
    param["status"] = current_user.status if current_user.is_authenticated else "Anonymous"
    param["username"] = current_user.name if current_user.is_authenticated else 0
    param["title"] = "Школьный форум"
    return render_template('index.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        currently = db_sess.query(User).filter(User.email == form.email.data).first()
        if currently is not None:
            if currently.check_password(form.password.data):
                login_user(currently, remember=form.remember_me.data)
                return redirect('/')
        else:
            return render_template('login.html', title="Авторизация", form=form,
                                   message="Пользователя с таким e-mail не найдено")
    return render_template('login.html', title="Авторизация", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Это имя уже занято")
        user = User(
            name=form.name.data,
            email=form.email.data,
            status=form.status.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title="Регистрация", form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
