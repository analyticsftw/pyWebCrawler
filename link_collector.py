#
# import libraries
#
import re
import numpy as np

from lxml import html
import requests
import progressbar

# import includes
import settings
import mysql_functions as myf
import support_functions as sf

mydb = myf.db_connect()


status_patterns = "(400)|(401)|(402)|(403)|(404)|(500)|(501)|(502)|(503)" 
max_pages = 1000
max_sites = 5000


sites = myf.get_unscanned(mydb, max_sites)
nresults = len(sites)


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

        try:
            tree = html.fromstring(page.content)
            links = tree.xpath('//a/@href')
            if len(links) == 0:
                myf.siteAssocRemove(mydb, nsite)
                myf.siteRemove(mydb, nsite)
                continue
            local_links = []
            external_links = []
            links = sf.sort_links(site, links)
            # keep uniques
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
