from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class Locate(Form):
    phone = TextField('phone', validators = [DataRequired()])
    name = TextField('name', validators = [DataRequired()])
    location = TextField('location', validators = [DataRequired()])
