#!/usr/bin/python
import os
credentials_file = os.path.join(os.path.dirname(__file__), "credentials.oracle")
if os.path.isfile(credentials_file):
    import database
    db = database.weather_database()
    db.upload()
else:
    print "credentials file not found"
