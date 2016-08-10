# Programmer: Brent Chambers
# Date: February 15, 2016
# Filename: assetGroupReport.py
# Technique: Asset Group Report Generator
# Syntax: assetGroupReport.py
# Description: Library for Fast Indexing of ATRIUM ASD Inventory Files

import os
import sys
import xlrd
import xlwt
import string
from datetime import datetime
import AtriumASD
import AtriumSTATS2
import QualysAccess
import shutil
import webbrowser
import time

instance = QualysAccess.Assets('pbm')

active_scans = ['Vuln Mgt Program - PBM HP NonStop',
'Authenticated RxConnect AZ',
'Vuln Mgt Program - RxAmerica Claims Adjudication',
'Authenticated - PBM IVR',
'Vuln Mgt Program - PBM iSeries Group A',
'Vuln Mgt Program - PBM MOP San Antonio',
'Vuln Mgmt Program - Internal Non-Production Assets from ASD',
'Rackspace Internal',
'Vuln Mgmt Program - Internal Production Assets from ASD',
'PBM DMZs',
'Vuln mgt program - PBM Legacy Standard Scan Assets',
'Authenticated - Non-Production',
'Authenticated - Production',
'Authenticated Production - Low Performance',
'PBM DVR',
'Vuln Mgt Program - PBM iSeries Group A']



htmlcode = "<h2>Qualys PBM Asset Group Report " + time.ctime() + "</h2>"
htmlcode += "<hr>"
htmlcode += "<h3> PBM Asset Groups </h3>"
htmlcode = "<h2>Qualys Asset Group Report " + time.ctime() + "</h2>"
htmlcode += "<hr>"
htmlcode += "<h3> PBM Asset Groups TOC </h3>"
for item in active_scans:
    htmlcode += "<a href=\"#" + item + "\">" + item + "</a><br>"
htmlcode += "<br>"
htmlcode += "<hr>"



for item in active_scans:
    assetsInGroup = instance.AssetDict[item]
    htmlcode += "<a name=\""+item+"\"></a>"
    htmlcode += "<b>ASSET GROUP: " + item + " </b> (Total Asset Count: " + str(len(instance.AssetDict[item])) + ")<br>"
    for i in assetsInGroup:
        htmlcode += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+i+"<br>"
    htmlcode += "<hr>"
file = open("pbm_asset_report.htm", 'w')
opener = "<html><head></head><body>"
closer = "</body></html>"
file.write(opener)
file.write(htmlcode)
file.write(closer)
file.close()
webbrowser.open("pbm_asset_report.htm")

    
