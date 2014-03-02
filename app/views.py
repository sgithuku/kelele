from os import environ
from flask import render_template, redirect, flash, request, url_for
from app import app
from forms import Locate
from forms import Intro
from twilio.rest import TwilioRestClient


from flask.ext.stormpath import (
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)

from stormpath.error import Error as StormpathError
app.config['SECRET_KEY'] = 'NotifyMe2014@friends'
app.config['STORMPATH_API_KEY_ID'] = environ.get('STORMPATH_API_KEY_ID')
app.config['STORMPATH_API_KEY_SECRET'] = environ.get('STORMPATH_API_KEY_SECRET')
app.config['STORMPATH_APPLICATION'] = environ.get('STORMPATH_APPLICATION')


stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = '.login'



@app.route('/', methods=('GET','POST'))
def index():
    form = Intro()
    if form.validate_on_submit():

        # Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = "AC0a825469aff4344dbf604f43ac9c2e39"
        auth_token  = "553bcc1ed54215ddc5739976ac6c7667"
        client = TwilioRestClient(account_sid, auth_token)
         
        message = client.sms.messages.create(body="Hi "+user.custom_data['contact_name1']+", "+ user.given_name+" just had an accident at "+form.location.data+" and may need your help.",
            to=user.custom_data['phone_number1'],    # Replace with your phone number
            from_="+16173000474") # Replace with your Twilio number
        message = client.sms.messages.create(body="Hi "+user.custom_data['contact_name2']+", "+ user.given_name+" just had an accident at "+form.location.data+" and may need your help.",
            to=user.custom_data['phone_number2'],    # Replace with your phone number
            from_="+16173000474") # Replace with your Twilio number
        print message.sid
        return redirect('/success')
    return render_template("intro.html", form=form)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This view allows a user to register for the site.

    This will create a new User in Stormpath, and then log the user into their
    new account immediately (no email verification required).
    """
    if request.method == 'GET':
        return render_template('register.html')

    try:
        # Create a new Stormpath User.
        _user = stormpath_manager.application.accounts.create({
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'given_name': request.form.get('given_name'),
            'surname': request.form.get('surname'),
        })
        _user.__class__ = User
    except StormpathError, err:
        # If something fails, we'll display a user-friendly error message.
        return render_template('register.html', error=err.message)

    login_user(_user, remember=True)
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This view logs in a user given an email address and password.

    This works by querying Stormpath with the user's credentials, and either
    getting back the User object itself, or an exception (in which case well
    tell the user their credentials are invalid).

    If the user is valid, we'll log them in, and store their session for later.
    """
    if request.method == 'GET':
        return render_template('login.html')

    try:
        _user = User.from_login(
            request.form.get('email'),
            request.form.get('password'),
        )
    except StormpathError, err:
        return render_template('login.html', error=err.message)

    login_user(_user, remember=True)
    return redirect(request.args.get('next') or url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    This view renders a simple dashboard page for logged in users.

    Users can see their personal information on this page, as well as store
    additional data to their account (if they so choose).
    """
    if request.method == 'POST':
        if request.form.get('contact_name1'):
            user.custom_data['contact_name1'] = request.form.get('contact_name1')
            user.custom_data['phone_number1'] = request.form.get('phone_number1')

        if request.form.get('contact_name2'):
            user.custom_data['contact_name2'] = request.form.get('contact_name2')
            user.custom_data['phone_number2'] = request.form.get('phone_number2')
        user.save()

    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    """
    Log out a logged in user.  Then redirect them back to the main page of the
    site.
    """
    logout_user()
    return redirect(url_for('index'))