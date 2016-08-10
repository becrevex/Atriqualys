# Programmer: Brent Chambers
# Date: February 4, 2016
# Filename: AtriumSTATS.py
# Technique: Statistic Generation of ATRIUM ASD Inventory Files
# Syntax:
# Description: Library for Analaysis and Trending of ATRIUM ASD Inventory Files

import sets
import xlwt
from datetime import datetime
from operator import itemgetter

font0 = xlwt.Font()
font0.name = "Times New Roman"
font0.color_index = 2
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0

style1 = xlwt.XFStyle()
style0.num_format_str = 'D-MMM-YY'

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

def returnNewRow():
        book = xlrd.open_workbook("c:\\Python27\\Qualys\\AtriumTracker.xls")
        sheet = book.sheet_by_name("A Test Sheet")
        newRow = ''
        for i in range(1,365):
                try:
                        print sheet.cell(2, i).__str__()
                except:
                        newRow = i
                        return newRow

def readStatistics():
        ''' Reads all the statistics from the AtriumTracker.xls file'''
        pass
        


def populateRecord(statlist):
    font0 = xlwt.Font()
    font0.name = "Times New Roman"
    font0.color_index = 2
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0
    style1 = xlwt.XFStyle()
    style0.num_format_str = 'D-MMM-YY'    
    column = returnNewRow()
    row = 3

    # Create timestamp field entry
    sheet.write(column, row, datetime.now(), style0)
    for item in statlist:
        sheet.write(row, column, item[0])
        row = row + 1


def createStatisticSnapshot():
	ws.write(0, 0, 'Atrium Asset Tracker v1.0', style0)
	ws.write(1, 1, datetime.now(), style0)
	recordNum = 2
	for item in newList:
		ws.write(recordNum, 0, item[0])		#key	
		ws.write(recordNum, 1, item[1])		#val
	ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('AtriumTracker.xls')

def remove_dupes(resource):
    unique_list = []
    collect = sets.Set(resource)
    for item in collect:
        unique_list.append(item)
    return unique_list


stat_struct = {"Record_Count":'',
               "Platform_Count":'',
               "Physical_System_Count":'',
               "Virtual_System_Count":'',
               "Server_Site_Count":'',
               "Deletion_Count":'',
               "StaticIP_Count":'',
               "Unique_OS_Count":'',
               "Unique_Orgs_Count":''}
               










class GenerateStats:
    asd = ''
    stats_list = []

    def __init__(self, asdInstance):
        self.asd=asdInstance
    def record_count(self):
        return len(self.asd.CurrentModeData)-2
    def platform_count(self):
        return len(remove_dupes(self.asd.Platform))
    def physical_system_count(self):
        return self.asd.SystemTypes.count("Physical")
    def virtual_system_count(self):
        return self.asd.SystemTypes.count("Virtual")
    def server_site_count(self):
        return len(remove_dupes(self.asd.Server_Site))
    def deletion_count(self):
        pass
    def staticIP_count(self):
        return len(remove_dupes(self.asd.IP_Address))
    def unique_os_count(self):
        return len(remove_dupes(self.asd.Operating_System_Version))
    def unique_orgs(self):
        return len(remove_dupes(self.asd.SupportOrgs))

    def systemsPerApplicationEnvironment(self):
        print "\nSystems Per each Application Environment"
        print "*************************"
        sysPerAppEnvironment = []
        for item in remove_dupes(self.asd.Application_Environment):
            sysPerAppEnvironment.append((item, self.asd.Application_Environment.count(item)))
            #print item + " "*(60-int(len(item))) + str(self.Platforms.count(item))
        sorted(sysPerAppEnvironment,key=itemgetter(1))
        for item in sorted(sysPerAppEnvironment,key=itemgetter(1)):
            print item[0] + " "*(60-int(len(item[0]))) + str(item[1])
        print "\n"

    def systemsPerPlatform(self):
        print "\nSystems Per each Platform"
        print "*************************"
        sysPerPlatform = []
        for item in remove_dupes(self.asd.Platform):
            sysPerPlatform.append((item, self.asd.Platform.count(item)))
            #print item + " "*(60-int(len(item))) + str(self.Platforms.count(item))
        sorted(sysPerPlatform,key=itemgetter(1))
        for item in sorted(sysPerPlatform,key=itemgetter(1)):
            print item[0] + " "*(60-int(len(item[0]))) + str(item[1])
        print "\n"

    def systemsPerServerSite(self):
        print "\nSystems Per each Server Site"
        print "****************************"
        sysPerServerSite = []
        for item in remove_dupes(self.asd.Server_Site):
            sysPerServerSite.append((item, self.asd.Server_Site.count(item)))
            #print item  + " "*(60-int(len(item))) + str(self.Sites.count(item))
        sysPerServerSite.sort()
        for item in sorted(sysPerServerSite,key=itemgetter(1)):
            print item[0] + " "*(60-int(len(item[0]))) + str(item[1])
        print "\n"

    def systemsPerOrg(self):
        print "\nSystems Per Each Support Organization"
        print "*************************************"
        sysPerSupportOrganization = []
        for item in remove_dupes(self.asd.SupportOrgs):
            sysPerSupportOrganization.append((item, self.asd.SupportOrgs.count(item)))
            #print item  + " "*(60-int(len(item))) + str(self.SupportOrgs.count(item))
        sysPerSupportOrganization.sort()
        for item in sorted(sysPerSupportOrganization, key=itemgetter(1)):
            print item[0] + " "*(60-int(len(item[0]))) + str(item[1])
        print "\n"

    def systemsPerOS(self):
        print "\nSystems Per Each Operating System"
        print "*********************************"
        sysPerOS = []
        for item in remove_dupes(self.asd.Operating_System_Version):
            sysPerOS.append((item, self.asd.Operating_System_Version.count(item)))
            #print item  + " "*(60-int(len(item))) + str(self.OperatingSystems.count(item))
        sysPerOS.sort()
        for item in sorted(sysPerOS, key=itemgetter(1)):
            print item[0] + " "*(60-int(len(item[0]))) + str(item[1])
        print "\n"        

        # Statistics should create a new workbook and record each entry with a timestamp as the column header
        # Every time statistics is created, it should create a new column and perform a comparison
                #the comparison should turn the color of the cell to red or green depending on whether
                #the value changed from the last time the system was ran.
    
