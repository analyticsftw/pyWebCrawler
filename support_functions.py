#
# Support functions
#
import re
import mysql_functions as myf


def clean_links(link, debug=0):
    # print("  Checking URL: " + link)
    pats: str = "(share?text)|(javascript:)|(mailto:)|(.(pdf|png|jpg|doc|xls|gif))|((\?|&)utm_)|(tel:)|\'"
    match = re.match(pats, link)
    if match is not None:
        if debug == 1: 
            # found match
            print("    Found match! --> " + match + " --> " + link)
        return True
    else:
        if debug == 1: 
            print("    Link is clean! --> " + link)
        return False


def find_host(url):
    chunks = url.split('/')
    newurl = chunks[0:3]
    return "/".join(newurl) + '/'


def sort_links(site, links):
    local_links = []
    external_links = []
    for link in links:
        if not (not (link == "") and not (link.startswith('tel:') is True) and not (
                link.startswith('javascript:') is True) and not (('#' not in link) is False)):
            continue
        if link.startswith('//') is True:
            # force HTTPS with relative protocols
            link = 'https:' + link
        if link.startswith('/') is True or link.startswith('http') is False:
            # relative link, add site
            if site.endswith('/'):
                link = site[:-1]+link
            else:
                link = site + link
            local_links.append(link)
            continue
        if link.find(site) != -1:
            # local site
            local_links.append(link)
        else:
            # external site
            external_links.append(find_host(link).lower())
    return [local_links, external_links]


def store_links(db_cursor, nsite, link_list, debug=1):
    local_links = link_list[0]
    external_links = link_list[1]

    for ll in local_links:
        check_link = clean_links(str(ll))
        if check_link is False:
            if myf.urlExists(db_cursor, ll) == 0:
                if debug == 1:
                    # not in database
                    print('  Not in URL database: ' + ll)
                    print ('  Adding: ' + ll)
                myf.urlInsert(db_cursor, nsite, ll)
            else:
                if debug == 1:
                    print('  Already in database')
        else:
            if debug == 1:
                print("  PROBLEM WITH %s" % str(ll))
    for el in external_links:
        site_check = myf.siteExists(db_cursor, el)
        if site_check == 0 and clean_links(str(el)) is False:
            if debug == 1:
                print("  Adding external site: " + el)
            si = myf.siteInsert(db_cursor, el)
            if myf.siteAssocExists(db_cursor, nsite, si) == 0:
                myf.siteAssoc(db_cursor, nsite, si)
        else:
            if debug == 1:
                print("  Site already in database: " + el)
    return "done"


def logMessage(p):
    fh = open("python.log", "a")
    fh.write(p+"\n")
    fh.close()