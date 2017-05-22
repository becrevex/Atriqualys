# Programmer: Brent Chambers
# Date: 4/9/2017
# Filename: QueueMgr.py
# Description:  Handles backend queue management for EQConsole ( Qualys Scan Queue and Automation ) QSQA

import os
import cgi
import cgitb
import string
import file_mgr
import datetime
import EQRequests
import QualysAccess

form = cgi.FieldStorage()
qa = QualysAccess.Assets('pbm')
Global_Records = []
scan_array = []


file_header = '''
Content-type:text/html\r\n\r\n
<html>
  <head>
     <title>EQ Console - Instance and Scanning Demo</title>
  </head>
<body>
'''

class Queue:
	scan_array = []
	scan_record_html = []
	header = ''
	record_table = ''
	footer = ''
	MainPage = ''
	lastUID = ''
	uidCount = '1001'

	def __init__(self):
		# when handler is created, it should grab the most recent uid and save it
		pass

	# Create new record
	def create_new_record(self, requester_name, server_ip, requester_email):
		text = "<h4>Vulnerability scan queued for %s, on %s for %s</h4>" % (requester_name, server_ip, requester_email)
		timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.datetime.now())
		file_mgr.write_record_to_queue(server_ip, requester_email, timestamp)
		file_mgr.commit_global_records()
		
	def create_new_schedule_record(self, uid, requester_name, domain, description, server_ip, requester_email, scan_date, scan_hour, scan_min):
		text = "<h4>Vulnerability scan queued for %s, on %s for %s</h4>" % (requester_name, server_ip, requester_email)
		timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.datetime.now())
		file_mgr.write_schedule_to_queue(uid, requester_name, domain, description, server_ip, requester_email, scan_date, scan_hour, scan_min)
		file_mgr.commit_global_records()

		#self.scan_array.append([requester_name, server_ip, requester_email, timestamp])
		# Stores record to record_tracker

	def create_new_record_dt(self, requester_name, server_ip, requester_email, network_domain, auth_type):
		timestamp = '{:%Y%m%d-%H:%M:%S}'.format(datetime.datetime.now())
		text =  "<h4>Vulnerability scan queued for %s, on %s for %s</h4>" % (requester_name, server_ip, requester_email)
		text += "<h4>Time requested: %s </h4>" % (timestamp)
		text += "<h4>Target: %s </h4>" % (server_ip)
		text += "<h4>Network Domain: %s </h4>" % (network_domain)
		text += "<h4>Authentication Type: %s </h4>" % (auth_type)
		Global_Records.append(requester_name, server_ip, requester_email, network_domain, auth_type, timestamp)
		# Stores record to record_tracker
		return text
		
		
	def save_record(self, uid, requester_name, server_ip, requester_email, timestamp):
		file_mgr.write_record_to_queue(uid, server_ip, requester_email, timestamp)
		file_mgr.commit_global_records()
		# Returns the header text to detail the scan
		return text

	def generate_record_html(self):
		html_collect = ''
		html_collect += '<table style=\"width:100%\">'
		for item in file_mgr.global_records:
			record = """<tr><th>""" + str(item[0]) + """</th><th>""" + str(item[1]) + """</th><th>""" + str(item[2]) + """</th><th>"""
			html_collect += record
		html_collect += "</table> "
		return html_collect
		
	def generate_schedule_html(self):
		html_collect = ''
		html_collect += '<table style=\"width:100%\">'
		for item in file_mgr.global_records:
			record = "<tr><th>"+ str(item[0]) +" </th>" + "<th>"+ str(item[1]) +"</th>" + "<th>"+ str(item[2]) +"</th>" + "<th>"+ str(item[3]) +"</th>" + "<th>"+ str(item[4]) +"</th>" + "<th>"+ str(item[5]) +"</th>" + "<th>"+ str(item[6]) +"</th>" + "<th>"+ str(item[7]) +"</th>" + "<th>"+ str(item[8]) +"</th></tr>"
			html_collect += record
		html_collect += "</table> "
		return html_collect

	
	def display_table_html(self):
	# Execute update page process
		page_html = ''
		page_html += self.header
		page_html += self.generate_record_html()
		page_html += self.footer
		self.MainPage = page_html
		print self.MainPage
		

	def launch_next_scan(self):
		target = file_mgr.global_records[-1][1]
		xl = qa.launch_vuln_scan("EQRequest_Queue_Scan", target)
		print xl


	def delete_record():
		scan_request = ''
		scan_request += self.header


	# Generate html from file