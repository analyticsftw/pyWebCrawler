#
# import libraries
#

from lxml import html
import numpy as np
import progressbar
import re
import requests
import settings
import sys

# import includes
import mysql_functions as myf
import support_functions as sf

# Initialize MySQL connection
mydb = myf.db_connect()


# Global variables

# for HTTP status codes
status_patterns = "(400)|(401)|(402)|(403)|(404)|(500)|(501)|(502)|(503)"

# Maximum sites to scan
max_sites = 10

# Maximum pages to scan per site
max_pages = 1000

# Grab command line argument for number of sites to scan
if len(sys.argv) == 2:
    max_sites = sys.argv[1]

# Get array of unscanned sites to scan
sites = myf.get_unscanned(mydb, max_sites)
nresults = len(sites)

# Walk through the list of URLs to crawl
with progressbar.ProgressBar(max_value=nresults) as bar:
    for i in range(0,len(sites)):
        site = sites[i][1]
        nsite = sites[i][0]
        sf.logMessage("Fetching: " + site)
        myf.siteUpdate(mydb, nsite)
        try:
            page = requests.get(site, timeout=5, headers=settings.headers)
            rem = re.search(status_patterns, str(page.status_code))
            if rem is not None:
                sf.logMessage ("ERROR: Found status code " + str(page.status_code))
                myf.siteAssocRemove(mydb, nsite)
                myf.siteRemove(mydb, nsite)
                continue

        # Extensive exception management for requests
        except requests.exceptions.ConnectionError:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("CANNOT CONNECT: " + site)
            pass
        except requests.exceptions.TooManyRedirects:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("TOO MANY REDIRECTS: " + site)
            pass
        except requests.exceptions.Timeout:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("TIMEOUT: " + site)
            pass
        except requests.exceptions.ChunkedEncodingError:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("INCOMPLETE READ: " + site)
            pass
        except requests.exceptions.ContentDecodingError:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("ENCODING ERROR: " + site)
            pass
        except requests.exceptions.SSLError:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("SSL ERROR: " + site)
            pass
        except requests.exceptions.InvalidSchema:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("SCHEMA ERROR: " + site)
            pass
        except requests.exceptions.MissingSchema:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("SCHEMA ERROR: " + site)
            pass
        except requests.exceptions.ContentDecodingError:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("DECODING ERROR: " + site)
            pass
        except requests.exceptions.InvalidURL:
            myf.siteAssocRemove(mydb, nsite)
            myf.siteRemove(mydb, nsite)
            sf.logMessage("REQUEST ERROR: " + site)
            pass

        # Assuming we passed the initial request, parse the HTML structure of the page
        try:
            tree = html.fromstring(page.content)
            links = tree.xpath('//a/@href')

            # If no links are found, remove site from database
            if len(links) == 0:
                myf.siteAssocRemove(mydb, nsite)
                myf.siteRemove(mydb, nsite)
                continue

            # Build arrays for local and external links
            local_links = []
            external_links = []

            # Sort arrays and keep uniques
            links = sf.sort_links(site, links)
            local_links = np.unique(links[0])
            external_links = np.unique(links[1])

            sf.logMessage("Found: " + str(len(local_links)) + " local links on " + site)
            sf.logMessage("Found: " + str(len(external_links)) + " external links on " + site)

            # Make an array of arrays
            store_links_array = [local_links, external_links]

            # Pass array to a link storing function
            store_links_action = sf.store_links(mydb, nsite, store_links_array, debug=0)
        except:
            pass

        # Update progress bar before iterating the loop
        bar.update(i)
