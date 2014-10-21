#!/usr/bin/python
import os
if os.path.isfile("credentials"):
    import database
    db = database.weather_database()
    db.upload()
else:
    print "credentials file not found"
