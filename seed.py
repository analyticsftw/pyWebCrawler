# import libraries
import sys
import numpy as np
# import urllib.request
# from bs4 import BeautifulSoup
from lxml import html
import requests
import mysql.connector

#import includes
import mysql_config as mycnf
import mysql_functions as myf
import support_functions as sf

mydb = mysql.connector.connect(
    host = mycnf.host,
    user = mycnf.user,
    passwd = mycnf.passwd,
    database = mycnf.database
)

# Enter your seed URL here
print(len(sys.argv))
if len(sys.argv)>1:
    site = sys.argv[1]
else:
    site = "https://msnbc.com"
page = requests.get(site + '/')

if sf.clean_links(site + "/") == False:
    if myf.siteExists(mydb, site) == 0:
        siteID = myf.siteInsert(mydb, site)
        print ("Site %s inserted with ID %s" % (site, str(siteID)))
        # insert site and return insert ID
    else:
        siteID = myf.siteGet(mydb, site)

tree = html.fromstring(page.content)
links = tree.xpath('//a/@href')
local_links = []
external_links = []
for link in links:
    if link == "":
        continue
    if link[0] == "/":
        # relative link, add site
        # print ("Relative: "+link)
        link = site + link
        local_links.append(link)
        continue
    if link[0] == "#":
        continue
    if link.find(site) != -1:
        # local site
        print ("Local: "+link)
        local_links.append(link)
    else:
        # external site
        print(link)
        external_links.append(sf.find_host(link).lower())

local_links = np.unique(local_links)
external_links = np.unique(external_links)

nll_added = 0
nel_added = 0
for ll in local_links:
    if sf.clean_links(ll) == False:
        if myf.urlExists(mydb, ll) == 0:
            print ("Adding: " + ll)
            myf.urlInsert(mydb, siteID,ll)
            nll_added = nll_added +1
for el in external_links:
    if sf.clean_links(el) == False:
        if myf.siteExists(mydb, el) == 0:
            si = myf.siteInsert(mydb, el)
            nel_added = nel_added + 1
            if myf.siteAssocExists(mydb, siteID, si) == 0:
                myf.siteAssoc(mydb, siteID, si)


print ("Seed sites added: " + str(nel_added))
