from flask import Flask, render_template, Response, redirect, url_for, request, flash
from mailin import Mailin
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, BooleanField, RadioField
from wtforms.fields.html5 import DateField
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = ''

class HomeQuote(Form):
    email = TextField('Email Address:') #, validators=[validators.required()])
    first_name = TextField('First Name:') #, validators=[validators.required()])
    last_name = TextField('Last Name:') #, validators=[validators.required()])
    birthdate = DateField('Birthdate:') #, validators=[validators.required()])
    married = BooleanField('Are you married?')
    spouse_first_name = TextField("Spouse's First Name:")
    spouse_last_name = TextField("Spouse's Last Name:")
    spouse_birthdate = DateField("Spouse's Birthdate:")
    autocomplete = TextField('What is your current address?')
    own_rent = RadioField('', choices=[('own','I own my current home'),('rent','I am renting')], default='own')
    homevalue = TextField('Estimated Value of your home (or loan amount):') #, validators=[validators.required()])
    newhomevalue = TextField('What is the purchase price?') #, validators=[validators.required()])
    aptunit = TextField('Apartment Number (if applicable)')
    new_purchase = RadioField('', choices=[('new','Are you purchasing a new home?'),('current','I want a quote for my current address')], default='current') #BooleanField('Is this a new purchase/rental?')
    autocomplete_new_purchase = TextField('What is the address of your new home?')

@app.route("/home", methods = ["POST", "GET"])
def home():
    if request.method == 'POST':
        form = HomeQuote(request.form, csrf_enabled=False)
        agent = request.form['agent']
        print(agent)

        invalid = ""
        styles = ""
        html = "<p>Completed home quote</p>"

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
            styles = " #spouse{display:block;} "
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
        
        if form.new_purchase.data:
            styles += " #new_purchase_address{display:block;} "
            html += "<p>New purchase? " + str(form.new_purchase.data) + "</p>"
            if form.autocomplete_new_purchase.data == "":
                invalid += "autocomplete_new_purchase,"
            else:
                html += "<p>Prior Address: " + str(form.autocomplete_new_purchase.data) + "</p>"


        invalid += "okay"

        if invalid == "okay":
            m = Mailin("https://api.sendinblue.com/v2.0", "")
            data = {
                "to": {str(form.email.data):str(form.first_name.data)},
                "from": ["freequote@utahinsurance.info", "Ryan Woolston"],
                "subject": "Free Home Quote",
                "html": html
            }
            result = m.send_email(data)
            print(result)
            return render_template("home_complete.html")
        else:
            flash('All fields are required.')
            invalids = invalid.split(',')
            return render_template("quote.html", form=form, agent=agent, invalids=invalids, styles=styles)
        
    else:
        agent = request.args.get('agent')
        form = HomeQuote(request.form)
        return render_template("quote.html", form=form, agent=agent)

@app.route("/api/home", methods = ["POST"])
def api_home():
    #content = request.get_json(force=True)
    return Response('{"response":"yes"}', status=200)

@app.route("/home_complete")
def home_complete():
    return render_template("home_complete.html")



if __name__ == "__main__":
    app.run()