import os
from flask import Flask, render_template, Response, redirect, url_for, request, flash
from mailin import Mailin
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField, RadioField
from wtforms.fields.html5 import DateField
from datetime import datetime
import appconfig as cfg
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__, static_url_path='/static', static_folder='')
app.config['SECRET_KEY'] = cfg.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQL_DB_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Quote(db.Model):
    __tablename__ = "quotes"
    quoteid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(25))
    email = db.Column(db.String(250))
    birthdate = db.Column(db.String(250))
    quote = db.Column(db.Text)
    

class HomeQuote(Form):
    email = TextField('Email Address:')
    first_name = TextField('First Name:')
    last_name = TextField('Last Name:')
    birthdate = DateField('Birthdate:')
    is_married = RadioField('', choices=[('', 'Yes, I am married or I have a domestic partner.'), ('single', "No, I am single")])
    spouse_first_name = TextField("Spouse's First Name:")
    spouse_last_name = TextField("Spouse's Last Name:")
    spouse_birthdate = DateField("Spouse's Birthdate:")
    current_address = TextField('What is your current address?')
    own_or_rent = RadioField('', choices=[('own', 'I own my current home'), ('rent', 'I am renting')], default='own')
    current_home_value = TextField('Estimated value of your home:')
    purchase_price = TextField('What is the purchase price?')
    aptunit = TextField('Apartment Number (if applicable)')
    is_new_purchase = RadioField('', choices=[('new', 'Yes, please quote my new home!'), ('current', "No, I'm looking for a better rate at my current address")])
    new_address = TextField('What is the address of your new home?')


class AutoQuote(Form):
    license = TextField('License')
    spouse_license = TextField('Spouse License')


def process_home(form):
    f = HomeQuote(form)
    d = json.dumps(form)
    print(d)
    html = ""
    m = Mailin("https://api.sendinblue.com/v2.0", cfg.SENDINBLUE_KEY)
    data = {
        "to": {str(f.email.data):str(f.first_name.data)},
        "from": ["freequote@utahinsurance.info", "Ryan Woolston"],
        "subject": "Free Home Quote",
        "html": d
    }
    result = m.send_email(data)

    id = int(datetime.now().strftime('%Y%m%d%H%M%S'))
    q = Quote(id, "HOME", f.email.data, f.birthdate.data, d)
    db.session.add(d)
    db.session.commit()

    return result
    

@app.route("/m/home", methods = ["POST", "GET"])
def home_mobile():
    if request.method == 'POST':
        form = HomeQuote(request.form, csrf_enabled=False)
        agent = request.form['agent']
        process_home(request.form)
        return render_template("home_mobile_complete.html")
    else:
        agent = request.args.get('agent')
        referred_by = request.args.get('ref')
        form = HomeQuote(request.form)
        return render_template("home_mobile.html", form=form, agent=agent, referred_by=referred_by)

@app.route("/home", methods = ["POST", "GET"])
def home():
    if request.method == 'POST':
        form = HomeQuote(request.form, csrf_enabled=False)
        agent = request.form['agent']
        process_home(request.form)
        return render_template("home_complete.html")
    else:
        agent = request.args.get('agent')
        referred_by = request.args.get('ref')
        form = HomeQuote(request.form)
        return render_template("home.html", form=form, agent=agent, referred_by=referred_by)

@app.route("/api/home", methods = ["POST"])
def api_home():
    #content = request.get_json(force=True)
    return Response('{"response":"yes"}', status=200)

@app.route("/home_complete")
def home_complete():
    return render_template("home_complete.html")


@app.route("/m/auto", methods = ["POST", "GET"])
def auto_mobile():
    if request.method == 'POST':
        form = AutoQuote(request.form, csrf_enabled=False)
        agent = request.form['agent']
    else:
        agent = request.args.get('agent')
        referred_by = request.args.get('ref')
        form = AutoQuote(request.form)
        return render_template("auto_mobile.html", form=form, agent=agent, referred_by=referred_by)

@app.route("/auto", methods = ["POST", "GET"])
def auto():
    if request.method == 'POST':
        print('wat')
    else:
        agent = request.args.get('agent')
        referred_by = request.args.get('ref')
        form = AutoQuote(request.form)
        return render_template("auto.html", form=form, agent=agent, referred_by=referred_by)

if __name__ == "__main__":
    app.run(debug=True)

