from flask import render_template, redirect, flash
from app import app
from forms import Locate
from twilio.rest import TwilioRestClient
from pyquery import PyQuery as pq
from lxml import etree
import urllib

@app.route('/')
def index():
 return render_template("intro.html")
@app.route('/success')
def success():
	return render_template("success.html")

# index view function suppressed for brevity

@app.route('/form', methods=('GET', 'POST'))
def form():
    form = Locate()
    if form.validate_on_submit():
        # Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = "AC0a825469aff4344dbf604f43ac9c2e39"
        auth_token  = "553bcc1ed54215ddc5739976ac6c7667"
        client = TwilioRestClient(account_sid, auth_token)
         
        message = client.sms.messages.create(body=form.name.data+" just had an accident  "+form.location.data+" and may need your help.",
            to=form.phone.data,    # Replace with your phone number
            from_="+16173000474") # Replace with your Twilio number
        print message.sid
        return redirect('/success')


    return render_template('form.html', form=form)

