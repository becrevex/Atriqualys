# Programmer: Brent Chambers
# Date: March 09, 2017
#  	Updates:  Added external and disaster recovery to the game!!!! (8/16/16)
# Filename: EthosAccess.py
# Technique: Accessing Ethos and Openstack via API Controls
# Syntax: (TBD)
# Description:  Authenticated access to openstack API RI cloud using personal credentials
#				in order to marry the functionality of Ethos/Openstack and QualysAPI scanning
'''
OpenStack Access Necessitites:
URL: http://10.228.128.16/horizon/project/
Username: bchambers2
Password: **************

Dependencies:  What a bunch of horse shit this was!!!!
Babel-2.3.4.tar.gz
beautifulsoup4-4.4.1.tar.gz
debtcollector-1.12.0.tar.gz
funcsigs-1.0.2.tar.gz
iso8601-0.1.11.tar.gz
keystoneauth1-1.1.0.tar.gz
monotonic-1.2.tar.gz
openstacksdk-0.9.14.tar.gz
oslo.i18n-3.13.0.tar.gz
oslo.serialization-2.17.0.tar.gz
oslo.utils-3.23.0.tar.gz
pbr-2.0.0.tar.gz
prettytable-0.7.2.tar.bz2
pyOpenSSL-0.15.1.tar.gz
python-libnmap-0.7.0.tar.gz
python-novaclient-7.1.0.tar.gz
qualysapi-4.1.0.tar.gz
sharepoint-0.4.2.tar.gz
urllib3-1.19.1.tar.gz
wrapt-1.10.8.tar.gz
stevedore-1.21.0.tar.gz
'''

# This almost worked.  Ran into some snags:


from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client

URL = "http://10.228.128.16:5000/v2.0"
USER = 'bchambers2'
PASS = **************
#PID  = 'sandbox'
PID  = "55b46aab43d94ede845317e3dd384793"

def setmeup():
	pop = Access()
	return pop


class Access:
	servers = []
	flavors = []
	networks = []
	api = ''
	nics = [("b276b562-108a-4f99-9f5e-31a229aaf9e9", "eb39f59c-f392-4b85-88b9-895840a6e0b5")]
	

	def __init__(self):
		loader = loading.get_plugin_loader('password')
		auth = loader.load_from_options(auth_url=URL, username=USER, password=PASS, project_id=PID)
		sess = session.Session(auth=auth)
		nova = client.Client('2.0', session=sess)
		self.api = nova

	def list_servers(self):
		for item in self.api.servers.list():
			self.servers.append(item)
		for item in self.servers:
			print item

	def list_images(self):
		pass
		
	def list_flavors(self):
		pass
		
	def list_networks(self):
		pass
		# shared_net-10.228.132.0-23 ==   "b276b562-108a-4f99-9f5e-31a229aaf9e9"
		# shared_subnet-10.228.132.0-23 =  b276b562-108a-4f99-9f5e-31a229aaf9e9
		# shared_net-10.228.129.0-24    = "eb39f59c-f392-4b85-88b9-895840a6e0b5"
		# shared_subnet-10.228.129.0-24 = "eb39f59c-f392-4b85-88b9-895840a6e0b5"
		for item in self.api.networks.findall():
			self.networks.append(item)
			self.nics.append(item)
		for network in self.networks:
			print network.label, "\t\t", network.id
	
	def create_new_server(self, name):
		flavor1 = self.api.flavors.list()[0]
		image1  = self.api.images.list()[0]
		nic1    = self.api.networks.list()[0]
		networks = []
		for item in self.api.networks.list():
			networks.append(item)
		self.api.servers.create(name, flavor=flavor1, image=image1, nics="auto")
		

	def create_new_instance(self, name, image="a0db7764-40ca-485c-aa85-e0e860bcea45", flavor="8783c20f-13ad-4d33-913e-516cae3542fa", 
			meta=None, 
			files=None, 
			reservation_id=None, 
			min_count=None, 
			max_count=None, 
			security_groups=None, 
			userdata=None, 
			key_name=None, 
			availability_zone=None, 
			block_device_mapping=None, 
			block_device_mapping_v2=None, 
			nics="auto", 
			scheduler_hints=None, 
			config_drive=None, 
			disk_config=None, 
			admin_pass=None, 
			access_ip_v4=None, 
			access_ip_v6=None):
		resp = self.api.servers.create(name, image, flavor,
						meta											=meta, 
						files											=files, 
						reservation_id									=reservation_id, 
						min_count										=min_count, 
						max_count										=max_count, 
						security_groups									=security_groups, 
						userdata										=userdata, 
						key_name										=key_name, 
						availability_zone								=availability_zone, 
						block_device_mapping							=block_device_mapping, 
						block_device_mapping_v2							=block_device_mapping_v2, 
						nics											="b276b562-108a-4f99-9f5e-31a229aaf9e9", 
						scheduler_hints									=scheduler_hints, 
						config_drive									=config_drive, 
						disk_config										=disk_config, 
						admin_pass										=admin_pass, 
						access_ip_v4									=access_ip_v4, 
						access_ip_v6									=access_ip_v6)
		return resp
			
		




