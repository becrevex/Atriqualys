# Programmer: Brent Chambers
# Date: February 15, 2016
# Filename: atriqualys.py
# Technique: Atriqualys ASD Inventory Files
# Syntax: atiqualys [Atrium ASD Excel File].xls
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


deconflict_dict = {'Retail DMZs':{},
'Vuln Mgt Program- Marketing Server Segment':{},
'Vuln mgt program - Retail Legacy Standard Scan Assets':{},
'Authenticated - TCS Offshore':{},
'Authenticated - Non-Production':{},
'Authenticated - Production':{},
'Vuln Mgmt Program - Internal Non-Production assets from ASD':{},
'Vuln Mgmt Program - Internal Production assets from ASD':{},
'External Retail Assets':{},
'Authenticated - RxConnect':{},
'Authenticated - TPMS':{},
'Vuln Mgt Program - Retail iSeries Group A':{},
'Vuln Mgt Program - RXConnect Production Servers':{},
'Authenticated - Low Intensity Devices':{},
'iLab':{}}


import datetime
import time

def compare(list1, list2):
    dupe_list = []
    for val in list1:
        if val in list2:
            dupe_list.append(val)
    return dupe_list


def count_sweep(list1):
    for item in list1:
        print item, len(instance.AssetDict[item])


def deconflict():
    # for each item in active scans
    for item in active_scans:
        print "------------------------------------------------------------+"
        print "[+] ASSET GROUP: ", item
        print "------------------------------------------------------------+"
        for i in active_scans:
            if item != i:
                results = compare(instance.AssetDict[item], instance.AssetDict[i])
                if (len(results) != 0):
                    print "\n     [" + str(len(results)) + "] Duplicate assets in " + i
            #print "Shared assets between " + "\'" + item + "\'" + " with Asset Group " + "\'" + i + "\'"
            
                for q in results:
                    print q
            #collect = {i:results}
        #deconflict_dict[item] = collect

    # Cleanly report the duplicates


def decon_report():
    htmlcode = "<h2>Qualys AssetGroup Asset Deconfliction Report " + time.ctime() + "</h2>"
    htmlcode += "<hr>"
    htmlcode += "<h3> Asset Groups </h3>"
    for item in active_scans:
        htmlcode += "<a href=\"#" + item + "\">" + item + "</a><br>"
    htmlcode += "<br>"
    htmlcode += "<hr>"

    
    for item in active_scans:
        htmlcode += "<a name=\""+item+"\"></a>"
        htmlcode += "<b>ASSET GROUP: " + item + " </b> (Total Asset Count: " + str(len(instance.AssetDict[item])) + ")<br>"
        htmlcode 
        #htmlcode += "<hr>"
        
        for i in active_scans:
            if item != i:
                results = compare(instance.AssetDict[item], instance.AssetDict[i])
                if (len(results) != 0):
                    htmlcode += "<br>\n     [<b>" + str(len(results)) + "</b>] Duplicate assets found in <b>" + i + "</b><br>"

                strandedIP = ''         #used for picking up straggling IPs or the Asset Groups with one host
                for q in results:
                        htmlcode += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+q+"<br>"
                #htmlcode += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+strandedIP+"<br>"
        htmlcode += "<hr>"
                

    file = open("decom_retail_report.htm", 'w')
    opener = "<html><head></head><body>"
    closer = "</body></html>"
    file.write(opener)
    file.write(htmlcode)
    file.write(closer)
    file.close()
    webbrowser.open("decom_retail_report.htm")


if __name__=='__main__':
	decon_report()




