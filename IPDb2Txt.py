#!/usr/env/python3

import os
import json
import requests

#If AbuseIPDB API key environment variable not set, exit.
if not os.environ['AbuseIPDB_API']:
	print('No API key set. Please create an Environment variable with the AbuseIPDB API key as the value')
	exit()

#If Reports file exists, remove it
if os.path.exists('reports.txt'): 
	os.remove('reports.txt')

#Setting current working directory and creating reports file
cwd = os.path.realpath(__file__)
new_cwd = cwd.replace(os.path.basename(__file__), "")

#Setting report file variable
report = new_cwd + 'reports.txt'

#Check for IP file, exit if not found
if not os.path.exists('ips.txt'):
	print('IP file not found. Please create a list of IPs in a txt file called "ips.txt"...')
	exit()

#Read IP file and append each IP to IP list
ips = []
ip_file = new_cwd + 'ips.txt'
with open(ip_file, 'r') as f: 
	file = f.read().split('\n')
	for ip in file:
		if ip == '':
			pass
		ips.append(ip)
f.close()

#For each IP in IP list, query AbuseIPDB Check API Endpoint and print results to reports file
for ip in ips:  
	url = 'https://api.abuseipdb.com/api/v2/check'
	headers = {
		'Accept': 'application/json',
		'key': '{}'.format(os.environ['AbuseIPDB_API'])
	}
	query = {'ipAddress': '{}'.format(ip)}
	request = requests.get(url, headers=headers, params=query)
	response = json.loads(request.text)
	with open(report, 'a') as f: 
		f.write(
			'IP: ' + str(ip) + '\n' +
			'Abuse Confidence Score: ' + str(response['data']['abuseConfidenceScore']) + '\n' +
			'Domain: ' + str(response['data']['domain']) + '\n' +
			'Country Code: ' + str(response['data']['countryCode']) + '\n' +
			'Report Link: ' + 'https://abuseipdb.com/check/' + str(ip) + ('\n' * 3) 
			)
		f.close()
#EzLife
