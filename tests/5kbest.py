#
# Use this script to seed your site search with websites from 5000best.com
# Be wary of adult sites!
# Usage: python 5kbest.py
#

# import libraries
import sys
import numpy as np
from lxml import html
import requests

# import includes
import settings
import mysql_functions as myf
import support_functions as sf

# Enter your seed URL here
site = "http://5000best.com/websites/"

# Create a database connection
mydb = myf.db_connect()

nloop = 2
while nloop != 50:
    
    site = "http://5000best.com/websites/" + str(nloop)
    # Request the URL
    page = requests.get(site, headers=settings.headers)

    # If page checks out, add URL to sites table
    if sf.clean_links(site + "/") == False:
        if myf.siteExists(mydb, site) == 0:
            siteID = myf.siteInsert(mydb, site)
            print ("Site %s inserted with ID %s" % (site, str(siteID)))
            # insert site and return insert ID
        else:
            print("Site already exists in sites table. Exiting.")
            exit()

    # After inserting the site's URL in the sites table,
    # process the URL's HTML to extract local and external links
    tree = html.fromstring(page.content)
    links = tree.xpath('//a/@href')
    local_links = []
    external_links = []
    for link in links:
        if link == "" or link[0:2] == "//":
            continue
        if link[0] == "/":
            # relative link, add site
            link = site + link
            local_links.append(link)
            continue
        if link[0] == "#":
            continue
        if link.find(site) != -1:
            # local link found
            print ("Local: "+link)
            local_links.append(link)
        else:
            # external link found
            external_links.append(sf.find_host(link).lower())

    # Process all links and remove duplicates

    local_links = np.unique(local_links)
    external_links = np.unique(external_links)

    nll_added = 0
    nel_added = 0

    for ll in local_links:
        if sf.clean_links(ll) == False:
            if myf.urlExists(mydb, ll) == 0:
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
    nloop = nloop + 1
# Done.

