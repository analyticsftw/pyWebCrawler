#
# Use this script to seed your site search
# Usage: python seed.py
# e.g. python seed.py
#

# import libraries

import progressbar
import mysql_functions as myf
from tld import get_tld

i = 0

# Create a database connection
mydb = myf.db_connect()

# get sites with no TLD
sql = "SELECT * FROM sites WHERE tld =''"
mycursor = mydb.cursor()
mycursor.execute(sql)
myresult = mycursor.fetchall()
mydb.close()

with progressbar.ProgressBar(max_value=len(myresult)) as bar:
    for item in myresult:
        id = str(item[0])
        url = item[1]
        try:
            myTLD=get_tld(url)
        except:
            myTLD='zzz'
        sqlUpdate = "UPDATE sites SET tld='" + myTLD + "' WHERE id='" + id + "'"
        # print(sqlUpdate)
        mydb = myf.db_connect()
        cursor = mydb.cursor()
        cursor.execute(sqlUpdate)
        mydb.commit()
        # Update progress bar before iterating the loop
        i = i + 1
        bar.update(i)
