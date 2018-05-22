import os
from flask import Flask, render_template, Response, redirect, url_for, request, flash
from mailin import Mailin
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField, RadioField
from wtforms.fields.html5 import DateField
from datetime import datetime
import appconfig as cfg
from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
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
    married = RadioField('', choices=[('','Yes, I am married or I have a domestic partner.'),('single',"No, I am single")])
    spouse_first_name = TextField("Spouse's First Name:")
    spouse_last_name = TextField("Spouse's Last Name:")
    spouse_birthdate = DateField("Spouse's Birthdate:")
    autocomplete = TextField('What is your current address?')
    own_rent = RadioField('', choices=[('own','I own my current home'),('rent','I am renting')], default='own')
    homevalue = TextField('Estimated value of your home:')
    purchase_price = TextField('What is the purchase price?')
    aptunit = TextField('Apartment Number (if applicable)')
    new_purchase = RadioField('', choices=[('new','Yes, please quote my new home!'),('current',"No, I'm looking for a better rate at my current address")])
    autocomplete_new_purchase = TextField('What is the address of your new home?')

class AutoQuote(Form):
    license = TextField('License')
    spouse_license = TextField('Spouse License')

def process_home(form):
    invalid = ""
    styles = ""
    scripts = ""
    html = "<p>Completed home quote</p>"

    if form.new_purchase.data == "new":
        styles += " #new_purchase_address{display:block;} #current_estimated_value{display:none;} "
        html += "<p>New purchase? " + str(form.new_purchase.data) + "</p>"
        if form.autocomplete_new_purchase.data == "":
            invalid += "autocomplete_new_purchase,"
        else:
            html += "<p>Prior Address: " + str(form.autocomplete_new_purchase.data) + "</p>"

    if form.first_name.data == "":
        invalid += "first_name,"
    else:
        html += "<p>Name: " + str(form.first_name.data)

    if form.last_name.data == "":
        invalid += "last_name,"
    else:
        html += " " + str(form.last_name.data) + "</p>"

    if form.email.data == "":
        invalid += "email,"
    else:
        html += "<p>" + str(form.email.data) + "</p>"

    if form.birthdate.data:
        birthdate = datetime.strptime(str(form.birthdate.data), '%Y-%m-%d')
        html += "<p>" + birthdate.strftime('%m/%d/%Y') + "</p>"
    else:
        invalid += "birthdate,"

    if form.married.data:
        styles += " #spouse{display:block;} "
        html += "<p>Married? " + str(form.married.data) + "</p>"
        if form.spouse_first_name.data == "":
            invalid += "spouse_first_name,"
        else:
            html += "<p>Spouse: " + str(form.spouse_first_name.data)

        if form.spouse_last_name.data == "":
            invalid += "spouse_last_name,"
        else:
            html += " " + str(form.spouse_last_name.data) + "</p>"

        if form.spouse_birthdate.data:
            spouse_birthdate = datetime.strptime(str(form.spouse_birthdate.data), '%Y-%m-%d')
            html += "<p>Spouse's birthday: " + spouse_birthdate.strftime('%m/%d/%Y') + "</p>"
        else:
            invalid += "spouse_birthdate,"

    if form.autocomplete.data == "":
        invalid += "autocomplete,"
    else:
        html += "<p>Address: " + str(form.autocomplete.data) + "</p>"


    # html += "<p>Own or rent: " + str(form.own_rent.data) + "</p>"
    
    if form.homevalue.data == "":
        invalid += "homevalue,"
    else:
        html += "<p>Home value: " + str(form.homevalue.data) + "</p>"

    # html += "<p>Apt Unit: " + str(form.aptunit.data) + "</p>"

    invalid += "okay"

    print(styles)

    if invalid == "okay":
        m = Mailin("https://api.sendinblue.com/v2.0", cfg.SENDINBLUE_KEY)
        data = {
            "to": {str(form.email.data):str(form.first_name.data)},
            "from": ["freequote@utahinsurance.info", "Ryan Woolston"],
            "subject": "Free Home Quote",
            "html": html
        }
        result = m.send_email(data)
        print(result)
        return invalid
    else:
        flash('All fields are required.')
        invalids = invalid.split(',')
        return invalids
    


@app.route("/m/home", methods = ["POST", "GET"])
def home_mobile():
    if request.method == 'POST':
        form = HomeQuote(request.form, csrf_enabled=False)
        agent = request.form['agent']
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
        
        inv = process_home(form)

        if inv == "okay":
            return render_template("home_complete.html")
        else:
            flash('All fields are required.')
            invalids = inv.split(',')
            return render_template("home.html", form=form, agent=agent, invalids=invalids, styles=styles, scripts=scripts)
        
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

