#!/usr/bin/python
import os
if os.path.isfile("credentials"):
    from database import *
    db = weather_database()
    db.upload()
else:
    print "credentials file not found"
