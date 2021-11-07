from django.db import models
from mongoengine import Document,fields
 

class Adresse(Document):
    location = fields.StringField()

    meta={
        'collection': 'station'
    }
     

