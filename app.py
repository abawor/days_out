from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('USER_ID')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
basic_auth = BasicAuth(app)


class DayOut(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    type = db.Column(db.String(100))
    cost = db.Column(db.Integer)
    rain = db.Column(db.String(1))
    dog = db.Column(db.String(1))
    time = db.Column(db.Integer)
    visited = db.Column(db.Boolean)


@app.route('/')
def index():
    # show all day out ideas
    day_out_list = DayOut.query.all()
    return render_template('home.html', day_out_list=day_out_list)


@app.route("/update/<string:day_out_id>")
@basic_auth.required
def update(day_out_id):
    # set existing item to visited/not visited
    day_out = DayOut.query.filter_by(id=day_out_id).first()
    day_out.visited = not day_out.visited
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=os.environ.get('APP_ENV', 'development') == 'development')
