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

deconflict_dict = {'Vuln Mgt Program - PBM HP NonStop':{},
'Vuln Mgt Program - RxAmerica Claims Adjudication':{},
'Authenticated - PBM IVR':{},
'Vuln Mgt Program - PBM iSeries Group A':{},
'Authenticated - PBM IVR':{},
'Vuln Mgt Program - PBM iSeries Group A':{},
'Vuln Mgt Program - PBM MOP San Antonio':{},
'Vuln Mgmt Program - Internal Non-Production Assets from ASD':{},
'Rackspace Internal':{},
'Vuln Mgmt Program - Internal Production Assets from ASD':{},
'PBM DMZs':{},
'Vuln mgt program - PBM Legacy Standard Scan Assets':{},
'Authenticated - Non-Production':{},
'Authenticated - Production':{},
'Authenticated Production - Low Performance':{},
'PBM DVR':{},
'Vuln Mgt Program - PBM iSeries Group A':{}}

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

                for q in results:
                    htmlcode += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+q+"<br>"
        htmlcode += "<hr>"
                

    file = open("decom_report.htm", 'w')
    opener = "<html><head></head><body>"
    closer = "</body></html>"
    file.write(opener)
    file.write(htmlcode)
    file.write(closer)
    file.close()
    webbrowser.open("decom_report.htm")
        


if __name__=='__main__':
	decon_report()
	





