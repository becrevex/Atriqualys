# Programmer: Brent Chambers
# Date: February 15, 2016
# Filename: retail_asset_groups.py
# Technique: Asset Group Report Generator
# Syntax: retail_asset_groups.py
# Description: HTML report of retail Asset Groups 

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

instance = QualysAccess.Assets('retail')

active_scans = ['Retail DMZs',
'Vuln Mgt Program- Marketing Server Segment',
'Vuln mgt program - Retail Legacy Standard Scan Assets',
'Authenticated - TCS Offshore',
'Authenticated - Non-Production',
'Authenticated - Production',
'Vuln Mgmt Program - Internal Non-Production assets from ASD',
'Vuln Mgmt Program - Internal Production assets from ASD',
'External Retail Assets',
'Authenticated - RxConnect',
'Authenticated - TPMS',
'Vuln Mgt Program - Retail iSeries Group A',
'Vuln Mgt Program - RXConnect Production Servers',
'Authenticated - Low Intensity Devices',
'iLab']

'''active_scans = ['Retail DMZs',
'Vuln Mgt Program- Marketing Server Segment',
'Vuln mgt program - Retail Legacy Standard Scan Assets',
'Authenticated - TCS Offshore',
'Authenticated - Non-Production',
'PCI Assets - 12/2014',
'Authenticated - Production',
'Vuln Mgmt Program - Internal Non-Production assets from ASD',
'Vuln Mgmt Program - Internal Production assets from ASD',
'External Retail Assets',
'Authenticated - RxConnect',
'Authenticated - TPMS',
'Vuln Mgt Program - Retail iSeries Group A',
'Vuln Mgt Program - RXConnect Production Servers',
'PCI 1/14/16',
'Daily PCI Asset Group',
'iLab']
'''

htmlcode = "<h2>Qualys Retail Asset Group Report " + time.ctime() + "</h2>"
htmlcode += "<hr>"
htmlcode += "<h3> Retail Asset Groups </h3>"
htmlcode = "<h2>Qualys Asset Group Report " + time.ctime() + "</h2>"
htmlcode += "<hr>"
htmlcode += "<h3> Retail Asset Groups TOC </h3>"
for item in active_scans:
    htmlcode += "<a href=\"#" + item + "\">" + item + "</a><br>"
htmlcode += "<br>"
htmlcode += "<hr>"



for item in active_scans:
    assetsInGroup = instance.AssetDict[item]
    htmlcode += "<a name=\""+item+"\"></a>"
    htmlcode += "<b>ASSET GROUP: " + item + " </b> " + "<br>"
    strandedIP = ''
    for i in assetsInGroup:
        if len(i) == 1:
            strandedIP += i
        else:
            htmlcode += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+i+"<br>"
    htmlcode += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" +strandedIP+"<br>"
    htmlcode += "<hr>"
file = open("retail_asset_report.htm", 'w')
opener = "<html><head></head><body>"
closer = "</body></html>"
file.write(opener)
file.write(htmlcode)
file.write(closer)
file.close()
webbrowser.open("retail_asset_report.htm")

    
