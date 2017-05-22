# Programmer: Brent Chambers
# Date: April 28, 2017
# Filename: LaunchScan.py 
# Technique: Command line utility to instantly launch vuln scan
# Syntax: LauncheScan.py <Title/Descrip> <target>
# Description:  Standard framework for working with qualys interface

import qualysapi
import xmltodict
from datetime import datetime
import warnings
import string
import sys
import QualysAccess
warnings.filterwarnings("ignore")

if len(sys.argv) < 3:
	print "Syntax: LaunchScan.py <biz_domain> <Title/Descrip> <target(s)>"
	print "Ex: LaunchScan.py [pbm|retail] \"DHI Adhoc-Scan WebIns20390\" 10.33.43.2-10.33.43.20"
	sys.exit()
else:
	biz_domain  = sys.argv[1]
	description = sys.argv[2]
	targetIPs   = sys.argv[3]

pbm_instance = QualysAccess.Assets('pbm')
retail_instance = QualysAccess.Assets('retail')

xdata = ''


if biz_domain == 'pbm' or biz_domain == "PBM":
	xdata = pbm_instance.launch_vuln_scan_default(description, targetIPs)
elif biz_domain == 'retail' or biz_domain == "RETAIL":
	xdata = retail_instance.launch_vuln_scan_default(description, targetIPs)
else:
	print biz_domain