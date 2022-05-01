from flask import Flask, render_template
from data import db_session
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
current_user = -1


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param["id"] = current_user.id
    param["avatar"] = current_user.avatar if current_user.avatar is not None else "avatars/id0.png"
    param["status"] = current_user.status
    param["username"] = current_user.name if current_user.name is not None else 0
    param["title"] = "Школьный форум"
    return render_template('index.html', **param)


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1).first()
    global current_user
    current_user = user
    app.run()


if __name__ == '__main__':
    main()
