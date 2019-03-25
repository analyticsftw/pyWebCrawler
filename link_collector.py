#
# import libraries
#
import re
import numpy as np
import urllib.request
from bs4 import BeautifulSoup
from lxml import html
import requests
import mysql.connector
import sys
import progressbar

#import includes
import mysql_config as mycnf
import mysql_functions as myf
import support_functions as sf



mydb = mysql.connector.connect(
    host=mycnf.host,
    user=mycnf.user,
    passwd=mycnf.passwd,
    database=mycnf.database
)


status_patterns = "(400)|(401)|(402)|(403)|(404)|(500)|(501)|(502)|(503)" 
max_pages = 1000
max_sites = 1000
mycursor = mydb.cursor()
sql = (
    "SELECT id, url FROM `sites` WHERE scanned=0 LIMIT 0," + str(max_sites)
)
mycursor.execute(sql)
myf.logQuery(mycursor)
myresult = mycursor.fetchall()
nresults = len(myresult)


with progressbar.ProgressBar(max_value=nresults) as bar:
    for i in range(0,len(myresult)):
        site = myresult[i][1]
        nsite = myresult[i][0]
        print("  Fetching: " + site)
        myf.siteUpdate(mydb, nsite)
        try:
            page = requests.get(site, timeout=5)
            rem = re.search(status_patterns, str(page.status_code))
            if rem is not None:
                print("  ERROR: Found status code " + str(page.status_code))
                myf.siteAssocRemove(mydb, nsite)
                myf.siteRemove(mydb, nsite)
                continue
            else:
                print ("  OK: Found status code " + str(page.status_code))
        except:
            print("  ERROR: " + site)
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            pass

        try:
            tree = html.fromstring(page.content)
            links = tree.xpath('//a/@href')
            if len(links) == 0:
                # print("  No links found")
                myf.siteAssocRemove(mydb, nsite)
                myf.siteRemove(mydb, nsite)
                continue
            local_links = []
            external_links = []
            links = sf.sort_links(site, links)
            # keep uniques
            local_links = np.unique(links[0])
            external_links = np.unique(links[1])

            print("  Found: " + str(len(local_links)) + " local links on " + site)
            print("  Found: " + str(len(external_links)) + " external links on " + site)
            store_links_array = [local_links, external_links]
            store_links_action = sf.store_links(mydb, nsite, store_links_array)
        except:
            pass
        bar.update(i)

