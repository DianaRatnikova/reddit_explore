from flask import Flask
from webapp.model import db, Top_Subreddit
from flask import render_template


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py') # откуда брать параметры конфигурации
    db.init_app(app)
    @app.route("/")

 #   def index():
    def index():
        return "Привет!"
    return app


if __name__=="__main__":
    app.run()