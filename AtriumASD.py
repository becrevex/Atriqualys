# Programmer: Rayshaw
# Date: February 4, 2016
# Filename: AtriumTEST.py
# Technique: Fast Indexing of ATRIUM ASD Inventory Files
# Syntax:
# Description: Library for Fast Indexing of ATRIUM ASD Inventory Files

import time

import xlrd
import xlwt
import sets
import string
import AtriumSTATS
from operator import itemgetter
from datetime import datetime

def get_datestamp():
	now = string.split(time.ctime())
	year   = now[-1]
	month  = now[1]
	day    = now[0]
	date   = now[2]
	creationStamp = year+"_"+month+"_"+day+"_"+date
	return creationStamp

def convert2string(ip_list):
        ips = ''
        for host in ip_list:
                ips += host + ', '
        ips = ips[:-1]
        return ips

def extractIPs(recordList):
        collect = []
        for item in recordList:
                collect.append(item[20])
        #print "Record count: ", len(recordList)
        #print "IP count:     ", len(collect)
        return collect

def remove_dupes(list):
        collect = []
        uniqueList = sets.Set(list)
        for item in uniqueList:
                collect.append(item)
        return collect

class ASD:
	filename = ''
	cache = ''
	book = ''
	creationStamp = ''
	Fields = {}
	RecordIndex = {}			#Field:[]
	start = 0
	stop = 0
	retail_host_list =[]
	retail_host_list_prod = []
	retail_host_list_nonprod = []
	pbm_host_list = []
	pbm_host_list_prod = []
	pbm_host_list_nonprod = []

	# Cache
	Business_Unit                   = []
        Application_Name                = []
        Application_Environment         = []
        PCI1A                           = []
        PCI1B                           = []
        PCI2A                           = []
        SOX	                        = []
        PII	                        = []
        PHI	                        = []
        SOC1                            = []
        SOC2                            = []
        RDC_A	                        = []
        RDC_P                           = []
        Exposure_Risk_Rating            = []
        DR_Tier                         = []
        Server_Name                     = []
        Server_Designation              = []
        Platform                        = []
        PLV_Hosted                      = []
        Server_Site                     = []
        IP_Address                      = []
        Operating_System_Version        = []
        Database_Name                   = []
        DB_Type                         = []
        DB_Version                      = []
        IT_Manager_First                = []
        IT_Manager_Last                 = []
        IT_Director_First               = []
        IT_Director_Last                = []
        Bus_Director_First              = []
        Bus_Director_Last               = []
        VP_POC_First                    = []
        VP_POC_Last                     = []
        IT_VP_First                     = []
        IT_VP_Last                      = []
        CurrentModeData = [Business_Unit,
                        Application_Name,
                        Application_Environment,
                        PCI1A,
                        PCI1B,	
                        PCI2A,	
                        SOX,	
                        PII,	
                        PHI,	
                        SOC1,	
                        SOC2,	
                        RDC_A,	
                        RDC_P,	
                        Exposure_Risk_Rating,
                        DR_Tier,
                        Server_Name,
                        Server_Designation,
                        Platform,	
                        PLV_Hosted,
                        Server_Site,
                        IP_Address,
                        Operating_System_Version,
                        Database_Name,
                        DB_Type,
                        DB_Version,
                        IT_Manager_First,
                        IT_Manager_Last,
                        IT_Director_First,
                        IT_Director_Last,
                        Bus_Director_First,
                        Bus_Director_Last,
                        VP_POC_First,
                        VP_POC_Last,
                        IT_VP_First,
                        IT_VP_Last]
	
	def __init__(self, filename="Atrium ASD Application Information 3-14-16.xlsx"):
                self.filename = filename
		self.creationStamp = get_datestamp()
		self.book = xlrd.open_workbook(self.filename)
		print "\nPopulating Atrium ASD Application fields..."
		self.populateFields()
		print "\nCreating records..."
		self.createRecordIndex()
		print "Populating records..."
		self.populateRecordIndex()
		print "Organizing sites..."
		self.organizeBySite()
		print "Populating record cache data..."
		self.populateData()
		print "Done."
		self.defineRange()



        def populateData(self):
                sheet = self.book.sheet_by_name("Export Worksheet")
        	Business_Unit                   = sheet.col_values(0)
        	Application_Name                = sheet.col_values(1)
                Application_Environment         = sheet.col_values(2)
                PCI1A                           = sheet.col_values(3)
                PCI1B                           = sheet.col_values(4)
                PCI2A                           = sheet.col_values(5)
                SOX	                        = sheet.col_values(6)
                PII	                        = sheet.col_values(7)
                PHI	                        = sheet.col_values(8)
                SOC1                            = sheet.col_values(9)
                SOC2                            = sheet.col_values(10)
                RDC_A	                        = sheet.col_values(11)
                RDC_P                           = sheet.col_values(12)
                Exposure_Risk_Rating            = sheet.col_values(13)
                DR_Tier                         = sheet.col_values(14)
                Server_Name                     = sheet.col_values(15)
                Server_Designation              = sheet.col_values(16)
                Platform                        = sheet.col_values(17)
                PLV_Hosted                      = sheet.col_values(18)
                Server_Site                     = sheet.col_values(19)
                IP_Address                      = sheet.col_values(20)
                Operating_System_Version        = sheet.col_values(21)
                Database_Name                   = sheet.col_values(22)
                DB_Type                         = sheet.col_values(23)
                DB_Version                      = sheet.col_values(24)
                IT_Manager_First                = sheet.col_values(25)
                IT_Manager_Last                 = sheet.col_values(26)
                IT_Director_First               = sheet.col_values(27)
                IT_Director_Last                = sheet.col_values(28)
                Bus_Director_First              = sheet.col_values(29)
                Bus_Director_Last               = sheet.col_values(30)
                VP_POC_First                    = sheet.col_values(31)
                VP_POC_Last                     = sheet.col_values(32)
                IT_VP_First                     = sheet.col_values(33)
                IT_VP_Last                      = sheet.col_values(34)

                for item in Business_Unit[2:]:
                        self.CurrentModeData[0].append(item)
                for item in Application_Name[2:]:	
                        self.CurrentModeData[1].append(item)
                for item in Application_Environment[2:]:
                        self.CurrentModeData[2].append(item)
                for item in PCI1A[2:]:
                        self.CurrentModeData[3].append(item)
                for item in PCI1B[2:]:
                        self.CurrentModeData[4].append(item)
                for item in PCI2A[2:]:
                        self.CurrentModeData[5].append(item)
                for item in SOX[2:]:
                        self.CurrentModeData[6].append(item)
                for item in PII[2:]:
                        self.CurrentModeData[7].append(item)
                for item in PHI[2:]:
                        self.CurrentModeData[8].append(item)
                for item in SOC1[2:]:	
                        self.CurrentModeData[9].append(item)
                for item in SOC2[2:]:
                        self.CurrentModeData[10].append(item)
                for item in RDC_A[2:]:	
                        self.CurrentModeData[11].append(item)
                for item in RDC_P[2:]:
                        self.CurrentModeData[12].append(item)
                for item in Exposure_Risk_Rating[2:]:
                        self.CurrentModeData[13].append(item)
                for item in DR_Tier[2:]:
                        self.CurrentModeData[14].append(item)
                for item in Server_Name[2:]:	
                        self.CurrentModeData[15].append(item)
                for item in Server_Designation[2:]:
                        self.CurrentModeData[16].append(item)
                for item in Platform[2:]:
                        self.CurrentModeData[17].append(item)
                for item in PLV_Hosted[2:]:
                        self.CurrentModeData[18].append(item)
                for item in Server_Site[2:]:
                        self.CurrentModeData[19].append(item)
                for item in IP_Address[2:]:
                        self.CurrentModeData[20].append(item)
                for item in Operating_System_Version[2:]:
                        self.CurrentModeData[21].append(item)
                for item in Database_Name[2:]:
                        self.CurrentModeData[22].append(item)
                for item in DB_Type[2:]:
                        self.CurrentModeData[23].append(item)
                for item in DB_Version[2:]:
                        self.CurrentModeData[24].append(item)
                for item in IT_Manager_First[2:]:
                        self.CurrentModeData[25].append(item)
                for item in IT_Manager_Last[2:]:	
                        self.CurrentModeData[26].append(item)
                for item in IT_Director_First[2:]:	
                        self.CurrentModeData[27].append(item)
                for item in IT_Director_Last[2:]:	
                        self.CurrentModeData[28].append(item)
                for item in Bus_Director_First[2:]:
                        self.CurrentModeData[29].append(item)
                for item in Bus_Director_Last[2:]:	
                        self.CurrentModeData[30].append(item)
                for item in VP_POC_First[2:]:
                        self.CurrentModeData[31].append(item)
                for item in VP_POC_Last[2:]:
                        self.CurrentModeData[32].append(item)
                for item in IT_VP_First[2:]:
                        self.CurrentModeData[33].append(item)
                for item in IT_VP_Last[2:]:
                        self.CurrentModeData[34].append(item)


                for item in Server_Name[2:]:
                        indexVal = Server_Name[2:].index(item)
                        self.CurrentModeData.append([item,
                                                     self.Business_Unit[indexVal],
                                                        self.Application_Name[indexVal],
                                                        self.Application_Environment[indexVal],
                                                        self.PCI1A[indexVal],
                                                        self.PCI1B[indexVal],
                                                        self.PCI2A[indexVal],	
                                                        self.SOX[indexVal],	
                                                        self.PII[indexVal],	
                                                        self.PHI[indexVal],	
                                                        self.SOC1[indexVal],	
                                                        self.SOC2[indexVal],	
                                                        self.RDC_A[indexVal],	
                                                        self.RDC_P[indexVal],	
                                                        self.Exposure_Risk_Rating[indexVal],
                                                        self.DR_Tier[indexVal],
                                                        self.Server_Designation[indexVal],
                                                        self.Platform[indexVal],	
                                                        self.PLV_Hosted[indexVal],
                                                        self.Server_Site[indexVal],
                                                        self.IP_Address[indexVal],
                                                        self.Operating_System_Version[indexVal],
                                                        self.Database_Name[indexVal],
                                                        self.DB_Type[indexVal],
                                                        self.DB_Version[indexVal],
                                                        self.IT_Manager_First[indexVal],
                                                        self.IT_Manager_Last[indexVal],
                                                        self.IT_Director_First[indexVal],
                                                        self.IT_Director_Last[indexVal],
                                                        self.Bus_Director_First[indexVal],
                                                        self.Bus_Director_Last[indexVal],
                                                        self.VP_POC_First[indexVal],
                                                        self.VP_POC_Last[indexVal],
                                                        self.IT_VP_First[indexVal],
                                                        self.IT_VP_Last[indexVal]])
                print "Imported " + str(len(self.CurrentModeData)) + " ASD records."
                                                     

				
	def defineRange(self):
		self.start = int(self.Fields.keys()[0])
		self.stop = int(self.Fields.keys()[-1])
				
	
	def populateFields(self):
		sheet = self.book.sheet_by_name("Export Worksheet")
		# Get the column titles from the page
		for i in range(0, 50):
			try:
				self.Fields[i]= sheet.cell(1,i).__str__()[7:-1] 		# because the cell object has a type lable (e.g 'text:')
			except:
				pass
		for item in self.Fields.values():
			print item
			
	def createRecordIndex(self):
		for item in self.Fields.values():
			self.RecordIndex[item] = []
	
	def populateRecordIndex(self):
		sheet = self.book.sheet_by_name("Export Worksheet")
		start = int(self.Fields.keys()[0])
		stop = int(self.Fields.keys()[-1]+1)
		print start, stop
		for column in range(start, stop):
			self.RecordIndex[self.Fields.keys()[column]] = sheet.col_values(column)

		
	def checkRecordImport(self):
		for column in range(int(self.start), int(self.stop)):
			print self.RecordIndex.keys()[column]#,":     ", len(self.RecordIndex[self.Fields[column]])
	
	# Data Retrival -- 
		
	def returnRecord(self, recordIndexVal):
		sheet = self.book.sheet_by_name("Export Worksheet")
		start = int(self.Fields.keys()[0])
		stop = int(self.Fields.keys()[-1]+1)		
		record = []
		for field in range(start, stop):
			record.append(self.RecordIndex[self.Fields.keys()[field]][recordIndexVal])
		# Run a len calculation to ensure all 
		return record

	def searchServers(self, query):
		masterResults = []
		searchResults = []
		searchServerResults = []
		serverSearchResults = []
		serverSearchResults = [ t for t in self.RecordIndex[15] if query in t ]

		for server in serverSearchResults:
				indexVal = self.RecordIndex[15].index(server)
				searchResults.append(self.returnRecord(indexVal))
		return searchResults


	def returnFieldfromRef(self, indexRef):
			try:
					#collect = self.RecordIndex[indexRef]            #grab the list
					name = self.Fields[indexRef]
			except:
					print "Could not find record, or record does not exist."
			return name

	def returnFieldRecords(self, indexRef, query):
			masterResults = []
			searchResults = []
			searchServerResults = []
			# Get the index number from the RecordIndex
			for item in self.RecordIndex[indexRef]:
					upperCaseValue = string.upper(item)
					splitCategory = string.split(upperCaseValue, " ")
					if string.upper(query) in splitCategory:
							searchResults.append(self.RecordIndex[indexRef].index(item))
			for item in searchResults:
					masterResults.append(self.returnRecord(item))
			return masterResults


	def organizeBySite(self):
		searchResults = []
		counter = int(0)
		for item in self.RecordIndex[19]:
			serverSite = string.split(item, " ")
			if "(DC)" in serverSite:
				self.retail_host_list.append(self.returnRecord(counter))
			elif "(DC" in serverSite:
				self.retail_host_list.append(self.returnRecord(counter))
			elif "(DC-" in serverSite:
				self.retail_host_list.append(self.returnRecord(counter))
			elif "CVS" and "Drive" in serverSite:
				self.retail_host_list.append(self.returnRecord(counter))
			elif "RI" and "2100" in serverSite:
				self.retail_host_list.append(self.returnRecord(counter))
			else:
				self.pbm_host_list.append(self.returnRecord(counter))
				counter = counter + 1

                #Remove duplicates, cause they're muckin up my statistics
		#self.retail_host_list = remove_dupes(extractIPs(self.retail_host_list))
		#self.pbm_host_list = remove_dupes(extractIPs(self.pbm_host_list))

		print "Parsing production retail hosts..."
		for item in self.retail_host_list:
			if item[2] == "Production":
				self.retail_host_list_prod.append(item)
			else:
				self.retail_host_list_nonprod.append(item)

		print "Parsing production pbm hosts..."
		for item in self.pbm_host_list:
			if item[2] == "Production":
				self.pbm_host_list_prod.append(item)
			else:
				self.pbm_host_list_nonprod.append(item)


		print "*************** Checks ******************"
		print "Retail Hosts Indexed:             " + str( len(self.retail_host_list))
		print "------------------------------------------"
		print "Retail - Production hosts:        " + str(len(self.retail_host_list_prod))
		print "Retail - Non-production hosts :   " + str(len(self.retail_host_list_nonprod))
		print "------------------------------------------"

		if str(len(self.retail_host_list_prod) + len(self.retail_host_list_nonprod)) == str( len(self.retail_host_list)):
			print "                Check Totals:     " + str(len(self.retail_host_list_prod) + len(self.retail_host_list_nonprod)) + " [GOOD]"
		else:
			print "                Check Totals:     " + str(len(self.retail_host_list_prod) + len(self.retail_host_list_nonprod)) + " INCONSISTENT"

		print "\n"
		print "PBM Hosts Indexed:                " + str(len(self.pbm_host_list))
		print "------------------------------------------"
		print "PBM - Production hosts:           " + str(len(self.pbm_host_list_prod))
		print "PBM - Non-production hosts:       " + str(len(self.pbm_host_list_nonprod))
		print "------------------------------------------"

		if str(len(self.pbm_host_list_prod) + len(self.pbm_host_list_nonprod)) == str(len(self.pbm_host_list)):
			print "                    Check Totals: " + str(len(self.pbm_host_list_prod) + len(self.pbm_host_list_nonprod)) + " [GOOD]"
		else:
			print "                    Check Totals: " + str(len(self.pbm_host_list_prod) + len(self.pbm_host_list_nonprod)) + " INCONSISTENT"
			
		print "\n"
		print "Consistency Check:"
		print "------------------------------------------"
		print "Total hosts indexed (RETAIL + PBM):   " + str(len(self.retail_host_list)+len(self.pbm_host_list))
		print "Compared to all records indexed:      " + str(len(self.RecordIndex[0]))
		print "\n\n"
