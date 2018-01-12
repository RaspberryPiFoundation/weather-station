# This program can be used to process and analyse data from your local MYSQL or
# MariaDB database. It looks ate air temperature and rainfall for 2017 but you should be able to modify it to
# process different weather measurements and other time periods.
# 
import MySQLdb
import calendar
import pprint
import operator
# Connect to local database - add your username and password
db=MySQLdb.connect(user="",passwd="",db="weather")
c = db.cursor() # Create a cursor

# Process Rainfall data
rainfall_avs={}
for mon in range(1,13): # Perform for every month
    c.execute("""select AVG(RAINFALL) from WEATHER_MEASUREMENT WHERE MONTH(CREATED) = %s AND YEAR(CREATED) = 2017;""",(mon,)) # Change the year if required
    r=c.fetchone()[0]
    if r:
        rainfall_avs[calendar.month_name[mon]] = float(r)
print("Average rainfall")
sorted_rainfall_avs= sorted(rainfall_avs.items(), key=operator.itemgetter(1))
pprint.pprint(sorted_rainfall_avs)
rainfall_tots={}
for mon in range(1,13): # Perform for every month
    c.execute("""select SUM(RAINFALL) from WEATHER_MEASUREMENT WHERE MONTH(CREATED) = %s AND YEAR(CREATED) = 2017;""",(mon,)) # Change the year if required
    r=c.fetchone()[0]
    if r:
        rainfall_tots[calendar.month_name[mon]] = float(r)
print("Total rainfall")
sorted_rainfall_tots= sorted(rainfall_tots.items(), key=operator.itemgetter(1))
pprint.pprint(rainfall_tots)
rainfall_max_av_month = max(rainfall_avs, key=lambda i: rainfall_avs[i])
rainfall_max_tots_month = max(rainfall_tots, key=lambda i: rainfall_avs[i])
print("Wettest month: " + str(rainfall_max_av_month) +" (average) " + str(rainfall_max_tots_month) +" (total) " )
rainfall_min_av_month = min(rainfall_avs, key=lambda i: rainfall_avs[i])
rainfall_min_tots_month = min(rainfall_tots, key=lambda i: rainfall_avs[i])
print("Driest month: " + str(rainfall_min_av_month) +" (average) " + str(rainfall_min_tots_month) +" (total) " )
c.execute("""select CREATED, RAINFALL from WEATHER_MEASUREMENT where RAINFALL=(select max(RAINFALL) from WEATHER_MEASUREMENT WHERE  YEAR(CREATED) = 2017);""")
r = c.fetchall()
print("Most rain in 5 minutes):") # Find heaviest downpour
for d in range(len(r)):
    print(str(r[d][0])+ " " + str(float(r[d][1])))

# Ambient temp
amb_temp_avs={}
for mon in range(1,13):
    c.execute("""select AVG(AMBIENT_TEMPERATURE) from WEATHER_MEASUREMENT WHERE MONTH(CREATED) = %s AND YEAR(CREATED) = 2017;""",(mon,))
    r=c.fetchone()[0]
    if r:
        amb_temp_avs[calendar.month_name[mon]] = float(r)
print("Average ambient temp")
sorted_amb_temp_avs= sorted(amb_temp_avs.items(), key=operator.itemgetter(1))
pprint.pprint(sorted_amb_temp_avs)
amb_temp_max_av_month = max(amb_temp_avs, key=lambda i: amb_temp_avs[i])
print("Hottest month: " + str(amb_temp_max_av_month) +" (average) "  )
amb_temp_min_av_month = min(amb_temp_avs, key=lambda i: amb_temp_avs[i])
print("Coolest month: " + str(amb_temp_min_av_month) +" (average) "  )
