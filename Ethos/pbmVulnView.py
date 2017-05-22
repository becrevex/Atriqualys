# Programmer: Brent Chambers
# Date: May 17, 2017
# Filename: pbmVulnView.py 
# Technique: Command line utility to view vulnerabilities of a PBM server
# Syntax: pbmVulnView.py <ipaddress>

import qualysapi
import xmltodict
from datetime import datetime
import warnings
import string
import sys
import QualysAccess
warnings.filterwarnings("ignore")

if len(sys.argv) <> 2:
	print "Syntax: pbmVulnView.py <ipaddress>"
	print len(sys.argv)
	sys.exit()
else:
	ipaddress  = sys.argv[1]

pbm_instance = QualysAccess.Assets('pbm')

pbm_instance.vuln_summary_tbl(ipaddress)

	

