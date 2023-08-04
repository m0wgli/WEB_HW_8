from mongoengine import *
import configparser
from urllib.parse import quote_plus

config = configparser.ConfigParser()

config.read('config.ini')

mongodb_url = config.get('DATABASE', 'mongodb_url')
mongodb_uri = quote_plus(mongodb_url)  # Екрануємо спеціальні символи у URL

connect(db='hw_8_2', host=mongodb_uri)

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    is_sent = BooleanField(default=False)