# purge!
import mysql.connector
import mysql_config
import sys

mydb = mysql.connector.connect(
    host = mysql_config.host,
    user = mysql_config.user,
    passwd = mysql_config.passwd,
    database = mysql_config.database
)
print (mysql_config.database)
mycursor = mydb.cursor()
sql = "TRUNCATE TABLE sites"
mycursor.execute(sql)
mydb.commit()
sql = "TRUNCATE TABLE sites_assoc"
mycursor.execute(sql)
mydb.commit()
sql = "TRUNCATE TABLE urls"
mycursor.execute(sql)
mydb.commit()
