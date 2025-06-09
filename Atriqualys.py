# Programmer: becrevex
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
from sets import Set

# Utility Functions

#ASD Output Parser

def remove_dupes(list):
        collect = []
        uniqueList = Set(list)
        for item in uniqueList:
                collect.append(item)
        return collect

def convert2string(ip_list):
        ips = ''
        for host in ip_list:
                ips += host + ','
        ips = ips[:-1]
        return ips


def ipcheck(ip_str):
    if len(ip_str.split()) == 1:
        ipList = ip_str.split('.')
        if len(ipList) == 4:
            for i, item in enumerate(ipList):
                try:
                    ipList[i] = int(item)
                except:
                    return False
                if not isinstance(ipList[i], int):
                    return False
            if max(ipList) < 256:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# ************* Qualys Management Commands ***********
# cmd: assets (Show all assets in the qualys subscription)

def show_assets():
	for item in qualys.list_ip_assets():
		print item
	print len(qualys.list_ip_assets()), "total assets associated with subscription."

# cmd: assetgroups (Show all assetgroups in the qualys subscription)
def show_assetgroups():
	qualys.list_asset_groups()
	
	'''
	ans = raw_input("First 100 Assets.  \nShow the rest? Y/N")
	if ans != "Y":
		return
	else:
		for item in qualys.list_asset_groups()[100:]:
			print item
	'''

def generate_stats():
        stats = AtriumSTATS2.GenerateStats(atrium)
        print "Record count:         ", stats.record_count()
        print "Platform count:       ", stats.platform_count()
        #print "Server site count:    ", stats.server_site_count()   Server site count:  Could not load supplied file... ???
        print "Unique IP count:      ", stats.staticIP_count()
        print "Unique OS count:      ", stats.unique_os_count()
        stats.systemsPerApplicationEnvironment()
        stats.systemsPerPlatform()
        stats.systemsPerServerSite()
        stats.systemsPerOS()
        qualys.statistics()

# KeyError: 'DEFAULT_APPLIANCE_ID':  File "QualysAccess.py", line 41, in build_data_structure
def reload_cache():
	qualys.build_data_structure()
	
def create_new_asset_group(name, ips):
	qualys.new_asset_group(name, ips)
	
def update_retail_groups(ASDObj):
	pass
	#qualys.new_asset_group(self, title, ips, comment="Created with qAPI", division="OPSEC", location="API_TEST")

def update_all():
        unique_retail_ASD_prod = remove_dupes(AtriumASD.extractIPs(atrium.retail_host_list_prod))
        unique_retail_ASD_nonprod = remove_dupes(AtriumASD.extractIPs(atrium.retail_host_list_nonprod))
        total_unique_retail = (unique_retail_ASD_prod + unique_retail_ASD_nonprod)

        unique_PBM_ASD_prod = remove_dupes(AtriumASD.extractIPs(atrium.pbm_host_list_prod))
        unique_PBM_ASD_nonprod = remove_dupes(AtriumASD.extractIPs(atrium.pbm_host_list_nonprod))
        total_unique_PBM = (unique_PBM_ASD_prod + unique_PBM_ASD_nonprod)


        print "-------------------------------------------------------"
        print "      Current Statistics (Prior to Updates)            "
        print "-------------------------------------------------------"
        print
        print '                                 ' + '   ASD     Qualys  '
        print '                                 ' + ' -------   -------  '
        print 'Retail production hosts:         ' + '| {:^6} | {:^6} |'.format(len(unique_retail_ASD_prod), len(qualys.AssetDict['Retail - Production']))
        print 'Retail non-production hosts:     ' + '| {:^6} | {:^6} |'.format(len(unique_retail_ASD_nonprod), len(qualys.AssetDict['Retail - NonProduction']))
        print '---------------------------------' + '  -----  | ------ |'
        print '                        Total:   ' + '| {:^6} | {:^6} |'.format((len(unique_retail_ASD_prod)+len(unique_retail_ASD_nonprod)),
                                                                               (len(qualys.AssetDict['Retail - Production']) + len(qualys.AssetDict['Retail - NonProduction'])))
        print
        print 'PBM production hosts:            ' + '| {:^6} | {:^6} |'.format(len(unique_PBM_ASD_prod), len(qualys.AssetDict['PBM - Production']))
        print 'PBM non-production hosts:        ' + '| {:^6} | {:^6} |'.format(len(unique_PBM_ASD_nonprod), len(qualys.AssetDict['PBM - NonProduction']))
        print '---------------------------------' + '  -----  | ------ |'
        print '                        Total:   ' + '| {:^6} | {:^6} |'.format((len(unique_PBM_ASD_prod)+len(unique_PBM_ASD_nonprod)),
                                                                               (len(qualys.AssetDict['PBM - Production']) + len(qualys.AssetDict['PBM - NonProduction'])))
                                                                               

        ans = raw_input("Update Asset Groups? (Y/N)")
        if string.upper(ans) != "Y":
                return
        else:
                update_all_retail()
                update_all_pbm()
                
                        


############################################################# Atrium Commands
def dump_retail_hosts():
        count = len(atrium.retail_host_list)
        for item in atrium.retail_host_list:
                print item
        print count, "retail hosts returned."

def dump_retail_hosts_prod():
        count = len(atrium.retail_host_list_prod)
        for item in atrium.retail_host_list_prod:
                print item
        print count, "production retail hosts returned."

def dump_retail_hosts_nonprod():
        count = len(atrium.retail_host_list_nonprod)
        for item in atrium.retail_host_list_nonprod:
                print item
        print count, "non-production retail hosts returned."

def dump_pbm_hosts():
        count = len(atrium.pbm_host_list)
        for item in atrium.pbm_host_list:
               print item
        print count, "pbm hosts returned."

def dump_pbm_hosts_prod():
        count = len(atrium.pbm_host_list_prod)
        for item in atrium.pbm_host_list_prod:
                print item
        print count, "production pbm hosts returned."

def dump_pbm_hosts_nonprod():
        count = len(atrium.pbm_host_list_nonprod)
        for item in atrium.pbm_host_list_nonprod:
                print item
        print count, "non-production PBM hosts returned."

# ######################################### Update Server Sites **************

# ALL Commands

def update_all_retail():
	update_retail_prod()
	update_retail_nonprod()

def update_all_pbm():
	update_pbm_prod()
	update_pbm_nonprod()

# RETAIL|PBM UPDATE Commands

def update_retail_prod():
	ips = qualys.AssetDict['Retail - Production']
	print "Retail - Production currently contains", len(ips), "assets."
	prodlist = Set(AtriumASD.extractIPs(atrium.retail_host_list_prod))
	u_list = []
	for item in prodlist:
                u_list.append(item)

        try:
                u_list.remove('0.0.0.0')
        except:
                pass
        prod_str = AtriumASD.convert2string(u_list)
        prod_str = prod_str[2:-1]
        qualys.edit_asset_group("Retail - Production", prod_str)
        qualys.build_asset_dict()
        new_ips = qualys.AssetDict['Retail - Production']
        print "Retail - Production now contains", len(new_ips), "assets."
	
def update_retail_nonprod():
	ips = qualys.AssetDict['Retail - NonProduction']
	print "Retail - NonProduction currently contains", len(ips), "assets."
	prodlist = Set(AtriumASD.extractIPs(atrium.retail_host_list_nonprod))
	u_list = []
	for item in prodlist:
                u_list.append(item)
        try:
                u_list.remove('0.0.0.0')
        except:
                pass
        prod_str = AtriumASD.convert2string(u_list)
        prod_str = prod_str[2:-1]
        qualys.new_asset_ip(prod_str)
        qualys.edit_asset_group("Retail - NonProduction", prod_str)
        qualys.build_asset_dict()
        new_ips = qualys.AssetDict['Retail - NonProduction']
        print "Retail - NonProduction now contains", len(new_ips), "assets."

def update_pbm_prod():
        prodlist = Set(AtriumASD.extractIPs(atrium.pbm_host_list_prod))
        u_list = []
        for item in prodlist:
                u_list.append(item)

        print sys.argv[1], "contains", len(u_list), "PBM Production IP addresses."

        ips = qualys.AssetDict['PBM - Production']              # Pull the current PBM Production content for persistence                
        print "Qualys Asset Group [PBM - Production] currently contains", len(ips), "assets."
        

        
        # Prep the string to update the asset group
        try:
                u_list.remove('0.0.0.0')
        except:
                pass
        prod_str = AtriumASD.convert2string(u_list)                # converts the IP list to a string
        prod_str = prod_str[2:-1]
        qualys.edit_asset_group("PBM - Production", prod_str)
        qualys.build_asset_dict()
        new_ips = qualys.AssetDict['PBM - Production']
        print "PBM - Production has been updated to contain", len(new_ips), "assets."
        
        
	
	
def update_pbm_nonprod():
	ips = qualys.AssetDict['PBM - NonProduction']
	print "PBM - NonProduction currently contains", len(ips), "assets."
	prodlist = Set(AtriumASD.extractIPs(atrium.pbm_host_list_nonprod))
	u_list = []
	for item in prodlist:
                u_list.append(item)
        try:
                u_list.remove('0.0.0.0')
        except:
                pass
        try:
                u_list.remove("IP Address")
        except:
                pass
        prod_str = AtriumASD.convert2string(u_list)
        prod_str = prod_str[2:-1]
        qualys.new_asset_ip(prod_str)
        qualys.edit_asset_group("PBM - NonProduction", prod_str)
        qualys.build_asset_dict()
        new_ips = qualys.AssetDict['PBM - NonProduction']
        print "PBM - NonProduction now contains", len(new_ips), "assets."


def serverSearch(self, query):
        masterResults = []
        searchResults = []
        serverSearchResults = []
        #serverSearchRestuls = [t for t in atrium.
	

# PIPE COMMANDS


# COMMAND LINE INTERFACE
def console():
	#os.system("cls")
	qualys = QualysAccess.Assets('pbm')

	print "\n\n"
	print r"      ATRIQUALYS        _          Atrium to Qualys Interface _ DST "
	print r" _______ _______  ______ _____  _____  _     _ _______        __   __ _______ "
	print r" |_____|    |    |_____/   |   |   __| |     | |_____| |        \_/   |______ "
	print r" |     |    |    |    \_ __|__ |____\| |_____| |     | |_____    |    ______| "
	print " "
	print r"                                                                version 1.0  "
	print " type 'help'"
	cmd = ''
	
	while (string.upper(cmd)) != ("QUIT" or "EXIT"):
		cmd = raw_input("\nPrompt#> ")
		command = string.split(cmd, " ")
		
		#Informational Commands
		if string.upper(command[0]) == "HELP" and len(command) <= 1:
			print __helpfile__
		elif string.upper(command[0]) == "ASSETS":						#> assets
			show_assets()
		elif string.upper(command[0]) == "STATS":
                        generate_stats()
		elif string.upper(command[0]) == "REFRESH":
                        print "Refreshing Qualys Asset Dictionary..."
                        qualys.build_asset_dict()
                        print "Done."
                        print "Refreshing Qualys Asset Group Index..."
                        qualys.update_asset_groups()
                        print "Done."
		elif string.upper(command[0]) == "ASSETGROUPS":						#> assetgroups 
			show_assetgroups()
		elif string.upper(command[0]) == "DELETE_GROUP":					#> deletegroup [groupName|groupID]
			pass
		elif string.upper(command[0]) == "DUMP" and len(command) <= 1:		#> dump (show syntax)
			print "Syntax: dump [retail|pbm] [prod|nonprod]"
		elif string.upper(command[0]) == "DUMP" and len(command) <= 2:		#> dump [retail|pbm]
			if string.upper(command[1]) == "RETAIL":
				dump_retail_hosts()
			elif string.upper(command[1]) == "PBM":
				dump_pbm_hosts()
			else:
				print "Syntax: dump [retail|pbm]"
		elif string.upper(command[0]) == "DUMP" and len(command) <= 3:		#> prod | nonprod
			if string.upper(command[1]) == "ALL":
				update_all()
			elif string.upper(command[1]) == "RETAIL" and string.upper(command[2]) == "PROD":
				dump_retail_hosts_prod()
			elif string.upper(command[1]) == "RETAIL" and string.upper(command[2]) == "NONPROD":
				dump_retail_hosts_nonprod()
			elif string.upper(command[1]) == "PBM" and string.upper(command[2]) == "PROD":
				dump_pbm_hosts_prod()
			elif string.upper(command[1]) == "PBM" and string.upper(command[2]) == "NONPROD":
				dump_pbm_hosts_nonprod()
			else:
				print "Syntax: dump [retail|pbm] [prod|nonprod]"

		# UPDATE Commands
		elif string.upper(command[0]) == "UPDATE" and len(command) <= 1:
			print "Syntax: update retail|pbm prod|nonprod"
		elif string.upper(command[0]) == "UPDATE" and len(command) <= 2:
                        if string.upper(command[1]) == "ALL":
                                update_all()
			elif string.upper(command[1]) == "RETAIL":
				update_all_retail()
			elif string.upper(command[1]) == "PBM":
				update_all_pbm()
			else:
				print "Syntax: update retail|pbm prod|nonprod"
		elif string.upper(command[0]) == "UPDATE" and len(command) >= 3:
			if string.upper(command[1]) == "RETAIL" and string.upper(command[2]) == "PROD":
					update_retail_prod()
			elif string.upper(command[1]) == "RETAIL" and string.upper(command[2]) == "NONPROD":
					update_retail_nonprod()
			elif string.upper(command[1]) == "PBM" and string.upper(command[2]) == "PROD":
					update_pbm_prod()
			elif string.upper(command[1]) == "PBM" and string.upper(command[2]) == "NONPROD":
					update_pbm_nonprod()
			else:
				print "Syntax: update [retail|pbm] [prod|nonprod]"
		elif string.upper(command[0]) == "UPDATE":
			update_all()                                    # Will need to create the persistent trending

                # ASSET GROUP MANAGEMENT COMMANDS
                elif string.upper(command[0]) == "CLEAR" and len(command) == 1:
                        print "Syntax: clear <assetgroup name>"
                        
		elif string.upper(command[0]) == "CLEAR" and len(command) >= 2:
                        try:
                                assetg = ' '.join(command[1:])
                                qualys.clear_asset_group(assetg)
                                qualys.build_asset_dict()
                                qualys.update_asset_groups()
                        except:
                                print "Syntax: clear <assetgroup name>"

                elif string.upper(command[0]) == "LIST" and len(command) == 1:
                        print "Syntax: list <assetgroup name>"

		elif string.upper(command[0]) == "LIST" and len(command) >= 2:
                        try:
                                assetg = ' '.join(command[1:])
                                print assetg
                                assets = qualys.AssetDict[assetg]
                                for item in assets:
                                        print item
                                print "\n", command[1], "contains", len(assets), "assets."
                        except:
                                print "Syntax: list <assetgroup name>"

                elif string.upper(command[0]) == "NEW" and len(command) <=2:
                        print "Syntax: new asset|ip <ip>"
                        print "Syntax: new assetgroup <assetgroup>"

		elif string.upper(command[0]) == "NEW" and len(command) >= 3:
			if string.upper(command[1]) == "ASSET" or "IP":
				try:
                                        qualys.new_asset_ip(command[2])
                                except:
                                        print "Syntax: new asset <ip>"
			elif string.upper(command[1]) == "ASSETGROUP":
				try:
                                        assetg = ' '.join(command[2:])
                                        print assetg
                                        qualys.new_empty_asset_group(command[2])
                                except:
                                        print "Syntax: new assetgroup <assetgroup name>"
                        else:
                                print "Syntax: new asset|ip <ip>"
                                print "Syntax: new assetgroup <assetgroup>"
                # Catch all
		else:
			pass
		


__helpfile__='''
Commands
--------
[+] Asset Group Managment Commands

help                            prints this nifty help file
assets                          view existing assets
assetgroups                     view existing asset groups
stats                           display stats on the loaded AtriumASD content
dump                            dump retail and pbm asset groups
update                          update retail and pbm asset groups
refresh                         refreshes cached assets and assetgroups
clear <assetgroup>              clears the asset contents of the supplied asset group
list <assetgroup>               lists the assets in the supplied asset group
new <assetgroup>                creates a new asset group
delete <assetgroup>             deletes the supplied asset group

'''

'''
if __name__=="__main__":
        if len(sys.argv) >= 2:
                try:
                        print "Loading ASD File Content..."
                        atrium = AtriumASD.ASD(sys.argv[1])
                        print "Loading Qualys Assets..."
                        qualys = QualysAccess.Assets()
                        #console()
                        update_all()
                except:
                        print "Could not load supplied file..."
                        sys.exit(1)
        else:
                print "Loading ASD File Content..."
                atrium = AtriumASD.ASD()
                print "Loading Qualys Assets... "
                qualys = QualysAccess.Assets()
        	console()
'''

if __name__=='__main__':
        print "Loading ASD File Content..."
        atrium = AtriumASD.ASD(sys.argv[1])
        print "Loading Qualys Assets..."
        qualys = QualysAccess.Assets()
        update_all()
