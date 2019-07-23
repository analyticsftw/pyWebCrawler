# pyWebCrawler
A Python POC project to crawl websites, list internal and external links on each site and establish site mapping of sorts

# Steps

* Create database called *webmap* and create tables. Use *webmap.sql* to create database structure.
* Update *mysql_config.py* with MySQL credentials
* Run *seed.py* either as-is or add a URL from the command line, e.g. 

  *python seed.py https://github.com*

Once you have enough entries in your *sites* table, run 

  *python link_collect.py* 

This will crawl all sites in *sites* table that have not yet been scanned and create an an association between *id_site1* (site where the external links were found) and *id_site2* (each external site ID)

# Notes
Activity / errors can be logged in *mysql.log* and *python.log* using functions in *mysql_functions.py* and *support_functions.py*
 

