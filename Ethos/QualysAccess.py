# Programmer: Brent Chambers
# Date: February 11, 2016
#  	Updates:  Added external and disaster recovery to the game!!!! (8/16/16)
# Filename: QualysAccess.py
# Technique: Creating Dynamic Asset Groups from Atrium
# Syntax: (TBD)
# Description:  Standard framework for working with qualys interface

import qualysapi
import xmltodict
import time
import warnings
import string
import os
from datetime import datetime
import xml.etree.ElementTree as ET


warnings.filterwarnings("ignore")

config_dict = {'test':'qualys_config.txt',
				'pbm':'qualys_config_pbm.txt',
				'retail':'qualys_config_retail.txt',
				'external':'qualys_config_ext.txt',
				'dr':'qualys_config_dr.txt',
				'null':'qualys_config_null.txt'}

# Converts a list of IPs/Ranges into a string for making
def convert2string(ip_list):
        ips = ''
        for host in ip_list:
                ips += host + ', '
        ips = ips[:-1]
        return ips


def range_expand(ip_range):
	collect = []
	#print "IP Range: ", ip_range
	try:
		ips = string.split(ip_range, "-")
	except:
		print ip_range, "is not an IP range."
	#print "Split IP: ", ips
	root_split = string.split(ips[0], ".")
	#print "Root split: ", root_split
	root = ''
	for item in root_split[:-1]:
		root += item + '.'
		#print "Root IP Address: ", root
	start = string.split(ips[0], ".")[-1]
	try:
		stop = string.split(ips[1], ".")[-1]
	except:
		print ips
	for item in range(int(start), int(stop)+1):
		range_ip = root + str(item)
		collect.append(range_ip)
	return collect

def rangeExpand(ip_range):
    collect = []
    ips = string.split(ip_range, "-")
    if len(ips) != 2:
        return
    root_split = string.split(ips[0], ".")          #takes the first IP and creates the 3 octects from that
    root = ''
    for item in root_split[:-1]:
        root += item + '.'                          #creates the 3 octect string for the IPs

    start = string.split(ips[0], ".")[-1]           #grabs the 4th octet to be the start of the range
    stop = string.split(ips[1], ".") [-1]           #grabs the 4th octet to be the stop of the range

    try:
        start_num = int(start)
        stop_num = int(stop)+1
        for item in range(start_num, stop_num):
            collect.append(root+str(item))
    except:
        pass
    return collect
        
    
                

class Assets:
	filename = "qualys_config.txt"
	api = ''
	AssetIndex  = []			# quick accessible list of assetsID:IP's
	AssetGroups = {}			# Keys: AssetGroupNames, Values: AssetGroupID
	AssetDict = {}              # Keys: AssetGroupNames, Values: List of IPs and Ranges
	scanner = ''
	qsub_v = ''
	fullpath = ''
	config_dict = {'test':'qualys_config.txt',
				'pbm':'qualys_config_pbm.txt',
				'retail':'qualys_config_retail.txt',
				'external':'qualys_config_ext.txt',
				'dr':'qualys_config_dr.txt',
				'null':'qualys_config_null.txt'}


	def __init__(self, qsub='test'):
		self.filename = self.config_dict[qsub]
		self.fullpath = os.getcwd()
		#full_config_filepath = self.fullpath.replace("\\", "\\\\") + "\\\\" + self.filename
		#print self.filename
		try:
			self.api = qualysapi.connect(self.filename)  	# Full path names and the config file?  WTF yo
			self.qsub_v = qsub
		except:
			print "\n[!] Please Authenticate: "
			#user = raw_input("Enter user: ")
			#passw = raw_input("Enter pass: ")
			try:
				self.api = qualysapi.connect("qualys.server.com")
			except:
				print "Could not connect.  Quitting..."
		#print "Loading asset groups..."
		#print "\nCVS-Qualys Instance Asset Groups as of " + str(datetime.now())
		#self.update_asset_groups()
		#self.build_asset_dict()


	def statistics(self):
		#Subscription Asset Group Count:
		#Asset Group Asset Count:
		for item in self.AssetDict.keys()[:2]:
			print item, "\t\t", len(self.AssetDict[item])

	def build_asset_dict(self):
		parameters = {'action': 'list'}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		collect = xdata['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']
		#Build the keys for the AssetDictionary
		AssetDict = {}
		for item in collect:
				AssetDict[item['TITLE']] = []
				try:
						ips = item['IP_SET']
						AssetDict[item['TITLE']] = ips
				except:
						pass
		for item in AssetDict.keys():
				if len(AssetDict[item]) == 2:
						IPS = []
						for ip in AssetDict[item]['IP']:
								IPS.append(ip)
						for ip_range in AssetDict[item]['IP_RANGE']:
								collect = rangeExpand(ip_range)
								if collect != None:
									for host in collect:
										IPS.append(host)
						#print "Total: ", len(IPS)        
						AssetDict[item] = IPS
				elif len(AssetDict[item]) == 1:
						try:
								AssetDict[item] = AssetDict[item]['IP']
						except:
								AssetDict[item] = AssetDict[item]['IP_RANGE']
								
				else:
						AssetDict[item] = []
		self.AssetDict = AssetDict

	# MANAGEMENT: Updates AssetGroups without printing them everytime.  
	def update_asset_groups(self):
		parameters = {'action': 'list'}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		for item in xdata['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']:
			self.AssetGroups[item['TITLE']] = item['ID']


                
        # ******** LIST AND DISPLAY FUNCTIONS ******

	# Lists Asset Group ID's and their corresponding names
	def list_asset_groups(self):
		parameters = {'action': 'list'}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		print "\nCVS-Qualys Instance Asset Groups as of " + str(datetime.now())
		for item in xdata['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']:
			print item['ID']+" : "+item['TITLE']
		print "\nLoaded " + str(len(xdata['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP'])) + " asset groups."


	#Prints just asset group ID's.  
	def list_asset_group_IDs(self):
		parameters = {'action': 'list'}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		for item in xdata['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']:
			print item["ID"]

	# Prints all host assets and their attributes:  [ID, IP, TRACKING_METHOD, DNS, NETBIOS, OS, QG_HOSTID
	def list_host_assets(self):
		parameters = {'action':'list',
					  'truncation_limit':'10000'}
		xmldata = self.api.request('/api/2.0/fo/asset/host', parameters)
		xdata = xmltodict.parse(xmldata)
		collect = []
		for item in xdata['HOST_LIST_OUTPUT']['RESPONSE']['HOST_LIST']['HOST']:
			print item
			collect.append(item)
		print "Returned", len(collect), " host assets."
		return collect


	# Prints just the IP's within the subscription.  Also returns IP's as a LIST.  
	def list_ip_assets(self):
		parameters = {'action':'list'}
		xmldata = self.api.request('/api/2.0/fo/asset/ip', parameters)
		xdata = xmltodict.parse(xmldata)
		ips = []
		ip_ranges = []
		collect = []
		for item in xdata['IP_LIST_OUTPUT']['RESPONSE']['IP_SET']['IP']:
			ips.append(item)
			collect.append(item)
		for item in xdata['IP_LIST_OUTPUT']['RESPONSE']['IP_SET']['IP_RANGE']:
			ip_ranges.append(item)
			collect.append(item)                # A future feature should be able to compute all IPs by calculating hosts within ranges
		return collect

# *********** Modify Asset Functions *************

	# Might work, but IP's need to be added to the subscription first
	def edit_asset_group(self, assetGroupName, ips, comment="Created with qAPI"):
		self.update_asset_groups()
		assetGroupID = self.AssetGroups[assetGroupName]
		parameters = {'action':'edit',
					'id':assetGroupID,
					'set_comments':comment,
					'add_ips':ips}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		#print xdata

	def clear_asset_group(self, assetGroupName, comment="Created with qAPI"):
		ips = convert2string(self.AssetDict[assetGroupName])
		ips = ips[:-1]
		assetGroupID = self.AssetGroups[assetGroupName]
		parameters = {'action':'edit',
					  'id':assetGroupID,
					  'set_comments':comment,
					  'remove_ips':ips}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		self.update_asset_groups()
		#print xdata

# ***************** Create New Asset Functions ***************

	def new_asset_ip(self, ip):
		parameters = {'action':'add',
					  'host_ips':ip}
		xmldata = self.api.request('/asset_ip.php', parameters)
		xdata = xmltodict.parse(xmldata)
		#print xdata
			

	# Not sure of the value of this.  
	def view_host_asset(self, ips, comment="Created with qAPI"):
		parameters = {'action':'list',
					  'ips':ips}
		xmldata = self.api.request('/api/2.0/fo/asset/host', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata


	# FIX = Broken, "No hosts queued for purging
	def del_host_asset(self, ips, comment="Created with qAPI"):
		parameters = {'action':'purge',
					  'ips':ips}
		xmldata = self.api.request('/api/2.0/fo/asset/host', parameters)
		xdata = xmltodict.parse(xmldata)
		print xdata

#                       --- 

	# Works like charm.  Now can you add existing IPs to it?
	def new_empty_asset_group(self, title, comment="Created with qAPI", division="OPSEC", location="API_TEST"):
		parameters = {'action':'add',
					'title':title,
					'comments':comment,
					'division':division,
					'location':location}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		print xmldata

	def new_asset_group(self, title, ips, comment="Created with qAPI", division="OPSEC", location="API_TEST"):
# Works like a charm, and adds new asset groups with IP's.  So if I can delete them, the problem is solved.  [
		parameters = {'action':'add',
			'title':title,
			'comments':comment,
			'division':division,
			'location':location,
			'business_impact':'High',
			'ips':ips} # Error 1905 - Invalid value for "<parameter>"
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		print xmldata


#   **************  Delete Functions ****************

	def del_asset_group_by_name(self, assetGroupName):
		self.update_asset_groups()
		try:
			assetGroupID = self.AssetGroups[assetGroupName]
		except:
			print "Error resolving assetGroupName.  Not found."
			return
		parameters = {'action':'delete','id':assetGroupID}
		xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata

	def del_asset_group_by_ID(self, assetGroupID):
		self.update_asset_groups()
		parameters = {'action':'delete','id':assetGroupID}
		try:
			xmldata = self.api.request('/api/2.0/fo/asset/group', parameters)
			xdata = xmltodict.parse(xmldata)
			print xdata
		except:
			print "Could not delete asset group."
			return
		print xdata['TEXT']

 
 #  ********************* Create and Initiate Scan Functions ************************

	def launch_vuln_scan_default(self, title, ip_address):
		optID = ''
		if self.qsub_v == "retail":
			scanner = 'is_cvscr_fw'
			optID   = '779264'
		elif self.qsub_v == "pbm":
			scanner = 'is_carem_fw'
			optID = '779436'
		parameters = {'action':'launch',
					'scan_title':title,
					'ip':ip_address,
					'option_id':optID,
					'iscanner_name':scanner}

		xmldata = self.api.request('/api/2.0/fo/scan', parameters)
		xdata = xmltodict.parse(xmldata)
		try:
			uID =  xdata['SIMPLE_RETURN']['RESPONSE']['ITEM_LIST']['ITEM'][0]['VALUE']
			print "\n\n[+] Scan Successfully Launched"
			print "\nConfirmation Number / Reference ID: ", uID
		except KeyError as ke:
			print ke
		#print xmldata
		return xdata


	def schedule_vuln_scan(self, title, ip_address):

		parameters = {'add_task': 'yes',   
						'scan_title': title,  
						'active': 'yes',  
						'type': 'scan',
						'scan_target':ip_address,
						'iscanner_name':'is_cvscr_fw',  
						#'asset_groups': asset_title,
						'scan_target': ip_address,
						#'scanners_in_ag': '1',  
						'option': 'Internal PCI Scan Options',  
						'occurrence': 'weekly',  
						'frequency_weeks': '1',  
						'weekdays': 'Tuesday',  
						'time_zone_code': 'US-GA',  
						'observe_dst': 'yes',  
						'start_hour': '11',  
						'start_minute': '15'}
		xmldata = self.api.request('scheduled_scans.php', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata
		

	def schedule_vuln_scan_tonight(self, title, ip_address, hour, min):

		parameters = {'add_task': 'yes',   
						'scan_title': title,  
						'active': 'yes',  
						'type': 'scan',
						'iscanner_name':'is_cvscr_fw',  
						'scan_target': ip_address,
						'option': 'Internal PCI Scan Options',  
						'occurrence': 'daily',  
						'frequency_days': '1',  
						#'weekdays': 'Tuesday',  
						'time_zone_code': 'US-GA',  
						'observe_dst': 'yes',  
						'start_hour': hour,  
						'start_minute': min}
		xmldata = self.api.request('scheduled_scans.php', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata

	def schedule_vuln_scan_by_datetime(self, title, ip_address, date, hour, min):
		if self.qsub_v == "retail":
			scanner = 'is_cvscr_fw'
		elif self.qsub_v == "pbm":
			scanner = 'is_carem_fw'
		else:
			scanner = 'auto'

		parameters = {'add_task': 'yes',   
						'scan_title': title,  
						'active': 'yes',  
						'type': 'scan',
						'iscanner_name':scanner,  #retail is default, change in args for other domains
						'scan_target': ip_address,
						'option': 'Internal PCI Scan Options',  
						'occurrence': 'daily',  
						'frequency_days': '1',  
						'start_date': date,  
						'time_zone_code': 'US-GA',  
						'observe_dst': 'yes',  
						'start_hour': hour,  
						'start_minute': min}
		xmldata = self.api.request('scheduled_scans.php', parameters)
		xdata = xmltodict.parse(xmldata)
		confNumber = ''
		#print xmldata
		# Ultimately, this last part checks the success of the scan by retrieving the referenceID.
		try:
			confNumber = xdata['SCHEDULEDSCANS']['SCAN']['@ref']
			#print "\n\n[+] Scan Successfully Scheduled"
			#print "\n\n Confirmation/Reference Number: ", confNumber
			return confNumber
		except KeyError as detail:
			print "No reference number returned."
			print detail
		return xdata



	def list_scheduled_scans(self):
		parameters = {'action':'list'}
		xmldata = self.api.request('scheduled_scans.php', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata
		
	
	def download_report(self, refID, description="ServerScan"):
		ts = time.time()
		st = datetime.fromtimestamp(ts).strftime('_%Y%m%d_%H-%M-%S')
		parameters = {
				   'action':'fetch',
				   'id':refID,
				   }
		print "Downloading the report ID: " + refID
		xmldata = self.api.request('/api/2.0/fo/report/', data=parameters)
		xdata = xmltodict.parse(xmldata)
		print "Writing new report..."
		with open("Scan_Report_"+ description + "_" + st + ".csv", "wb") as report:
			report.write(xmldata.content)
	'''
		def list_reports(self):
			parameters = {
					   'action':'list',
					   }
			xmldata = self.api.request('/api/2.0/fo/report/', data=parameters)
			xdata = xmltodict.parse(xmldata)
			records = []
			report_list = xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT'][5]
			for item in xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT']:
				try: 
					count = 
					report_id	 	= xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT'][report_list..index(item)]['ID']
					report_date  	= xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT'][report_list.index(item)]['LAUNCH_DATETIME']
					report_title 	= xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT'][report_list.index(item)]['TITLE']
					report_format 	= xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT'][report_list.index(item)]['OUTPUT_FORMAT']
					report_expires 	= xdata['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT'][report_list.index(item)]['EXPIRATION_DATETIME']
					record = [report_id, report_date, report_title, report_format, report_expires]
				#print record[0]," "*25-int(len(record[0])),
				#		record[1], " "*25-int(len(record[1])),
				#		record[2], " "*25-int(len(record[2])),
				#		record[3], " "*25-int(len(record[3])),
				#		record[4], " "*25-int(len(record[4]))
					records.append(record)
				except KeyError:
					pass
			for rec in records:
				print rec[0]," "*25-int(len(rec[0])), \
						rec[1], " "*25-int(len(rec[1])), \
						rec[2], " "*25-int(len(rec[2])), \
						rec[3], " "*25-int(len(rec[3])), \
						rec[4], " "*25-int(len(rec[4]))
			return xdata
	'''
	def downloadReport(self, refID, description="ServerScan"):
		import requests
		s = requests.Session()
		s = requests.Session()
		s.headers.update({'X-Requested-With':'Support Free Info Agent v2.1'})
		payload = {
				   'action':'login',
				   'username':'cvsca_bc2',
				   'password':'*********'
				   }		
		r = s.post('https://qualysapi.qualys.com/api/2.0/fo/session/', data=payload)
		xmlreturn = ET.fromstring(r.text)
		for elem in xmlreturn.findall('.//TEXT'):
			print elem.text
			ts = time.time()
		st = datetime.fromtimestamp(ts).strftime('_%Y%m%d_%H-%M-%S')
		payload = {
			   'action':'fetch',
			   'id':refID,
			   }
		print "Downloading the report associated with... " + refID
		r = s.post('https://qualysapi.qualys.com/api/2.0/fo/report/', data=payload)
		print "Writing CSV report..."
		with open(refID + "_" + description + st + ".csv", "wb") as report:
			report.write(r.content)
		print "Done."
		print "Writing PDF Report..."
		with open(refID + "_" + description + st + ".pdf", "wb") as report:
			report.write(r.content)
		print "Done."
			
			
#  ********************* Create and Download Report Functions *****************************

	
	def launch_pdf_report(self, ips):
		_allvulns = "1881638"	
		parameters = {'action':'launch','ips':ips,'template_id':_allvulns,'output_format':'pdf'}
		xmldata = self.api.request('/api/2.0/fo/report', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata
		return xdata
		
	def launch_cvs_report(self, ips):
		_allvulns = "1881638"
		parameters = {'action':'launch','ips':ips,'template_id':_allvulns,'output_format':'pdf'}
		xmldata = self.api.request('/api/2.0/fo/report', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata
		return xdata
	
#  ********************* VM Detection Tools *****************************

	def vuln_summary(self, ips):
		parameters = {'action':'list','ips':ips}
		xmldata = self.api.request('/api/2.0/fo/asset/host/vm/detection', parameters)
		xdata = xmltodict.parse(xmldata)
		print xmldata
		return xdata
		
	def vuln_summary_tbl(self, ips):
		parameters = {'action':'list','ips':ips}
		xmldata = self.api.request('/api/2.0/fo/asset/host/vm/detection', parameters)
		xdata = xmltodict.parse(xmldata)
		try:
			host_ID = xdata['HOST_LIST_VM_DETECTION_OUTPUT']['RESPONSE']['HOST_LIST']['HOST']['ID']
		except:
			host_ID = "Not found."
		try:
			host_IP = xdata['HOST_LIST_VM_DETECTION_OUTPUT']['RESPONSE']['HOST_LIST']['HOST']['IP']
		except:
			host_IP = "Not found."
		try:
			vuln_count = len(['HOST_LIST_VM_DETECTION_OUTPUT']['RESPONSE']['HOST_LIST']['HOST']['DETECTION_LIST']['DETECTION'])
		except:
			vuln_count = 0
		
		vulnerabilities = []
		for item in xdata['HOST_LIST_VM_DETECTION_OUTPUT']['RESPONSE']['HOST_LIST']['HOST']['DETECTION_LIST']['DETECTION']:
			try:
				qid = item['QID']
			except:
				qid = 'Not found.'
			try:
				severity = item['SEVERITY']
			except:
				severity = 'Not found.'
			try:
				descrip  = item['RESULTS']
			except:
				descrip = 'Not found.'
				
			vulnerabilities.append((severity, qid, descrip))
		
		vuln_count = len(vulnerabilities)
		vulnerabilities.sort(reverse=True)
		print "\n"
		print "Host ID:    ", host_ID
		print "Host IP:    ", host_IP
		print "Vuln count: ", vuln_count
		print "\n"
		print " QID     SEV     RESULTS  "
		print "-----    ---     -------  "
		for row in vulnerabilities:
			d1 = string.replace(row[2], "\t", " ")
			d2 = string.replace(d1, "\n", " ")
			print row[1], " "*(8-int(len(row[1]))), row[0], " "*(8-int(len(row[1]))), (d2[:90])
		print "-----"
			
			
			
		

		#return xdata
