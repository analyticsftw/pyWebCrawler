#
# MySQL support functions
#

import datetime
import mysql.connector
import mysql_config as myc


def db_connect():
    mydb = mysql.connector.connect(
        host=myc.host,
        user=myc.user,
        passwd=myc.passwd,
        database=myc.database
    )
    return mydb


def get_unscanned(p, max_sites):
    mycursor = p.cursor()
    sql = "SELECT id, url FROM `sites` WHERE scanned=0 LIMIT 0," + str(max_sites)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    logQuery(mycursor)
    return myresult


def insertURL(p,id_site,url):
    mycursor = p.cursor()
    sql = "INSERT INTO urls (id_site, url) VALUES (%s, %s);"
    val = (str(id_site), url)
    mycursor.execute(sql, val)
    logQuery(mycursor)
    p.commit()


def siteGet(p,url):
    mycursor = p.cursor()
    sql = "SELECT id from sites WHERE url =  '"+ url +"' LIMIT 0,1;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    logQuery(mycursor)
    return (myresult[0][0])


def siteExists(p,url):
    mycursor = p.cursor()
    sql = "SELECT id from sites WHERE url =  '"+ url +"';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    logQuery(mycursor)
    return (len(myresult))


def siteIdExists(p,id):
    mycursor = p.cursor()
    sql = "SELECT id, url from sites WHERE id =  '"+ str(id) +"';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    logQuery(mycursor)
    return (myresult[0][1])


def siteInsert(p, url):
    p# rint("  Inserting site: " + url)
    mycursor = p.cursor()
    sql = "INSERT INTO sites (url) VALUES ('" + url + "')"
    mycursor.execute(sql)
    logQuery(mycursor)
    p.commit()
    return mycursor.lastrowid


def siteAssoc(p,id_site1, id_site2):
    mycursor = p.cursor()
    sql = "INSERT INTO sites_assoc (id_site1, id_site2) VALUES (%s, %s);"
    val = (str(id_site1), str(id_site2))
    mycursor.execute(sql, val)
    p.commit()
    sql = "INSERT INTO sites_assoc (id_site1, id_site2) VALUES (%s, %s);"
    val = (str(id_site2), str(id_site1))
    mycursor.execute(sql, val)
    logQuery(mycursor)
    p.commit()


def siteAssocExists(p,id_site1, id_site2):
    mycursor = p.cursor()
    sql = "SELECT id_assoc from sites_assoc WHERE (id_site1 = %s AND id_site2 = %s) OR (id_site1 = %s AND id_site2 = %s);"
    val = (str(id_site1), str(id_site2), str(id_site2), str(id_site1))
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    logQuery(mycursor)
    return (len(myresult))


def siteAssocRemove(p,id_site):
    # print ("  Removing assocs for site ID " + str(id_site))
    mycursor = p.cursor()
    sql = "DELETE FROM sites_assoc WHERE (id_site1 = %s OR id_site2 = %s);"
    val = (str(id_site), str(id_site))
    mycursor.execute(sql, val)
    logQuery(mycursor)
    p.commit()   


def siteUpdate(p,id_site):
    # print ("  Removing site ID " + str(id_site))
    mycursor = p.cursor()
    ds = datetime.datetime.now()
    dst = ds.strftime("%Y-%m-%d %H-%M-%S")
    sql = "UPDATE sites SET scanned=1,date='" + dst + "' WHERE id = " + str(id_site)
    mycursor.execute(sql)
    logQuery(mycursor)
    p.commit()


def siteRemove(p,id_site):
    print ("  Removing site ID " + str(id_site))
    mycursor = p.cursor()
    sql = "DELETE FROM sites WHERE id = " + str(id_site)
    val = (str(id_site))
    mycursor.execute(sql)
    logQuery(mycursor)
    p.commit()


def urlInsert(p,id_site,url):
    # print ("  Inserting URL: " + url)
    mycursor = p.cursor()
    sql = (
        "INSERT INTO urls (id_site, url) "
        "VALUES (%s, %s)"
    )
    val = (str(id_site), str(url))
    mycursor.execute(sql, val)
    logQuery(mycursor)
    p.commit()


def urlExists(p,url):
    mycursor = p.cursor()
    sql = "SELECT id from urls WHERE url =  '"+ url + "';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # print ("  Found " + str(len(myresult)) + " results")
    logQuery(mycursor)
    return len(myresult)


def urlGet(p,id_site,url):
    mycursor = p.cursor()
    sql = "SELECT id from urls WHERE id_site =  '" + id_site + "';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # print ("Found " + str(len(myresult)) + " results")
    logQuery(mycursor)
    return len(myresult)

def logQuery(p):
    fh = open("mysql.log", "a")
    fh.write(p.statement+"\n")
    fh.close()