# Programmer: Brent Chambers
# Date: April 27, 2017
# Filename: ScheduleScan.py 
# Technique: Command line utility to schedule QualyScan
# Syntax: ScheduleScan.py <Title/Descrip> <target> <date> <hour> <min>
# Description:  Standard framework for working with qualys interface

import qualysapi
import xmltodict
from datetime import datetime
import warnings
import string
import sys
import QualysAccess
warnings.filterwarnings("ignore")

cool_hours = ['23','00','0','00','01','02','03','04','05']

if len(sys.argv) < 6:
	print "\nQualys CLI Scan Scheduler v1.0"
	print "------------------------------"
	print "Syntax: ScheduleScan.py <biz_domain> <Title/Descrip> <target(s)> <date> <hour> <min>"
	print "\nEx: ScheduleScan.py [pbm|retail] \"DHI Adhoc-Scan WebIns20390\" 10.33.43.2-10.33.43.20 04/30/2017 23 06"
	print "-------------------------------------------------->"
	sys.exit()

elif sys.argv[5] not in cool_hours:
	print "Please schedule scan between acceptable scan window (23:00-06:00)"
	sys.exit()	
	
else:
	biz_domain  = sys.argv[1]
	description = sys.argv[2]
	targetIPs   = sys.argv[3]
	date	    = sys.argv[4]
	hour	    = sys.argv[5]
	min 	    = sys.argv[6]

pbm_instance = QualysAccess.Assets('pbm')
retail_instance = QualysAccess.Assets('retail')

xdata = ''


if biz_domain == 'pbm' or biz_domain == "PBM":
	xdata = pbm_instance.schedule_vuln_scan_by_datetime(description, targetIPs, date, hour, min)
elif biz_domain == 'retail' or biz_domain == "RETAIL":
	xdata = retail_instance.schedule_vuln_scan_by_datetime(description, targetIPs, date, hour, min)
else:
	print biz_domain	

