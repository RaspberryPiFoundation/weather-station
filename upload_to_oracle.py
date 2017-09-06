#!/usr/bin/python3
import os, fcntl
credentials_file = os.path.join(os.path.dirname(__file__), "credentials.oracle")
if os.path.isfile(credentials_file):
    lock_file = "/var/lock/oracle.lock"
    f = open(lock_file, 'w')
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("No other uploads in progress, proceeding...")
        import database # requires MySQLdb python 2 library which is not ported to python 3 yet
        db = database.weather_database()
        db.upload()
    except IOError:
        print("Another upload is running exiting now")
    finally:
        f.close()
else:
    print("Credentials file not found")
