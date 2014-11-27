#!/usr/bin/python
import os, fcntl
credentials_file = os.path.join(os.path.dirname(__file__), "credentials.oracle")
if os.path.isfile(credentials_file):
    lock_file = "/var/lock/oracle.lock"
    f = open(lock_file, 'w')
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print "no other uploads in progress, proceeding..."
        import database
        db = database.weather_database()
        db.upload()
    except IOError:
        print "another upload is running exiting now"
    finally:
        f.close()
else:
    print "credentials file not found"
