from flask import Flask, render_template
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    username_from_db = 0
    param = {}
    param["id"] = 1
    param["avatar"] = "avatars/id1.png"
    param["status"] = "ученик"
    param["username"] = username_from_db
    param["title"] = "Школьный форум"
    return render_template('index.html', **param)


def main():
    app.run()


if __name__ == '__main__':
    main()
