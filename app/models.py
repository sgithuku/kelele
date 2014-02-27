from app import db
import datetime

class User(db.DynamicDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	username = db.StringField(max_length=255, required=True, unique=True)
	email = db.EmailField(max_length=255, required=True, unique=True)
	first_name = db.StringField(max_length=255, required=True)
	last_name = db.StringField(max_length=255, required=False)
	phone = db.IntField(max_length=255, required=True)
	number1 = db.IntField(max_length=255, required=True)
	number2 = db.IntField(max_length=255, required=False)

	def __unicode__ (self):
		return self.first_name
