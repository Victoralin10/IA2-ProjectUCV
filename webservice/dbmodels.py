
from pynamodb import models, attributes


class User(models.Model):
    class Meta:
        table_name = "ucv.users"
        region = "us-east-1"

    username = attributes.UnicodeAttribute(hash_key=True)
    email = attributes.UnicodeAttribute()
    password = attributes.UnicodeAttribute()
    firstName = attributes.UnicodeAttribute(null=True)
    lastName = attributes.UnicodeAttribute(null=True)
    audio = attributes.JSONAttribute()
