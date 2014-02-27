from flask import Flask

app = Flask(__name__)
app.config.from_object('config')


if __name__ == "__main__":
 app.run(port=5011,debug = True)

from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

DB_NAME = 'test'
DB_USERNAME = 'kelele'
DB_PASSWORD = 'kelele'
DB_HOST_ADDRESS = '/usr/local/var/mongodb'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

app.config["\x94\xd66Dk\x04\xa9\x18\xc7\xd4@w\xd9\xb1\xb8\xb3\xa2U\xec\xe8\x1d\xd3\xf6\xc0"]


from app import views, models