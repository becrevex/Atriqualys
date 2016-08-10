# Programmer: Brent Chambers
# Date: February 11, 2016
# Filename: QualysAccess.py
# Technique: Creating Dynamic Asset Groups from Atrium
# Syntax: (TBD)
# Description:  Standard framework for working with qualys interface

import qualysapi
import xmltodict
from datetime import datetime
import warnings
import string
warnings.filterwarnings("ignore")

config_dict = {'test':'qualys_config.txt',
            'pbm':'qualys_config_pbm.txt',
            'retail':'qualys_config_retail.txt',
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
	AssetDict = {}                          # Keys: AssetGroupNames, Values: List of IPs and Ranges


	def __init__(self, qsub='test'):
                self.filename = config_dict[qsub]
		try:
			self.api = qualysapi.connect(self.filename)
		except:
			print "Config file missing or connect failed."
			user = raw_input("Enter user: ")
			passw = raw_input("Enter pass: ")
			try:
				self.api = qualysapi.connect("qualys.server.com")
			except:
				print "Could not connect.  Quitting..."
		print "Loading asset groups..."
		print "\nCVS-Qualys Instance Asset Groups as of " + str(datetime.now())
		self.update_asset_groups()
		self.build_asset_dict()


        def statistics(self):
            #Subscription Asset Group Count:
            #Asset Group Asset Count:
            for item in self.AssetDict.keys():
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

        #
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
    
    
