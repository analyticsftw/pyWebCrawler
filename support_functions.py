#
# Support functions
#
import re

import mysql_functions as myf


def clean_links(link):
    # print("  Checking URL: " + link)
    pats = "(share?text)|(javascript:)|(mailto:)|(.(pdf|png|jpg|doc|xls|gif))|((\?|&)utm_)|(tel:)|\'"
    match = re.match(pats, link)
    if match is not None:
        # found match
        # print("    Found match!")
        return True
    else:
        # print("    Link is clean")
        return False


def find_host(url):
    chunks = url.split('/')
    newurl = chunks[0:3]
    return "/".join(newurl) + '/'


def sort_links(site, links):
    local_links = []
    external_links = []
    print ('  SORTING...')
    for link in links:
        if not (not (link == "") and not (link.startswith('tel:') is True) and not (
                link.startswith('javascript:') is True) and not (('#' not in link) is False)):
            continue
        if link.startswith('//') is True:
            link = 'https:' + link
        if link.startswith('/') is True or link.startswith('http') is False:
            # relative link, add site
            # print ('Relative: ' + link)
            if site.endswith('/'):
                link = site[:-1]+link
            else:
                link = site + link
            local_links.append(link)
            continue
        if link.find(site) != -1:
            # local site
            # print ('Local: ' + link)
            local_links.append(link)
        else:
            # external site
            external_links.append(find_host(link).lower())
    return [local_links, external_links]


def store_links(db_cursor, nsite, link_list, debug=0):
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
            print("  PROBLEM WITH %s" % str(ll))

    for el in external_links:
        site_check = myf.siteExists(db_cursor, el)
        if site_check == 0 and clean_links(str(el) == False):
            if debug == 1:
                print ("  Adding external site: " + el)
            si = myf.siteInsert(db_cursor, el)
            if myf.siteAssocExists(db_cursor, nsite, si) == 0:
                myf.siteAssoc(db_cursor, nsite, si)
        else:
            if debug == 1:
                print("  Site already in database: " + el)

