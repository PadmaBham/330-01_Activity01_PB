"""
Scripts to run to set up our database
"""

from passlib.hash import pbkdf2_sha256
from datetime import datetime
from model import db, User, Task


# Create the database tables for our model
db.connect()
db.drop_tables([User, Task])
db.create_tables([User, Task])

# User(username="user1", password="password1").save()
 
Task(task="Do the laundry.").save()
Task(task="Do the dishes.", performed=datetime.now()).save()

User(username="admin", password=pbkdf2_sha256.hash("password")).save()
User(username="bob", password=pbkdf2_sha256.hash("bobbob")).save()
