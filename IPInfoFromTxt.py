#!/usr/env/python3

import os
import re
import json
import requests
import webbrowser

#If AbuseIPDB API key environment variable not set, exit.
if not os.environ.get('abuseipdbkey'):
	print('No AbuseIPDB API key set. Please create an Environment variable with the AbuseIPDB API key as the value')
	exit()

#If Reports text/html file exists, remove it
if os.path.exists('reports.txt'): 
	os.remove('reports.txt')

if os.path.exists('reports.html'):
	os.remove('reports.html')

#Setting current working directory and creating reports file
cwd = os.path.realpath(__file__)
new_cwd = cwd.replace(os.path.basename(__file__), "")

#Setting report/HTML file variable
report = new_cwd + 'reports.txt'
html_file = new_cwd + 'reports.html'

#Check for IP file, exit if not found
if not os.path.exists('ips.txt'):
	print('IP file not found. Please create a list of IPs in a txt file called "ips.txt in the same directory as this script')
	exit()

#Create first part of the HTML file
with open(html_file, 'w') as f:
	f.write(
		'<html>' + '\n' +
		'  <head>' + '\n' +
		'    <title>IP Address Information</title>' + '\n' +
		'    <style>' + '\n' +
		'      body {' + '\n' +
		'        background-color: #cccccc;' + '\n' +
		'        text-align: center;' + '\n' +
		'      }' + '\n' +
		'      table {' + '\n' +
		'        margin: 0 auto;' + '\n' +
		'        border-collapse: collapse;' + '\n' +
		'		 border: 1px solid black;' + '\n' +
		'      }' + '\n' +
		'      th {' + '\n' +
		'        background-color: #FF8000;' + '\n' +
		'        padding: 10px;' + '\n' +
		'      }' + '\n' +
		'      td {' + '\n' +
		'		 border: 1px solid black;' + '\n' +
		'		 background-color: #FFFFFF;' + '\n' +
		'        padding: 10px;' + '\n' +
		'      }' +	 '\n' +
		'    </style>' + '\n' +
		'  </head>' + '\n' +
		'  <body>' + '\n' +
		'    <h1>IP Address Information</h1>' + '\n' +
		'    <table>' + '\n' +
		'      <tr>' + '\n' +
		'        <th>IP</th>' + '\n' +
		'        <th>Abuse Confidence Score</th>' + '\n' +
		'        <th>Domain</th>' + '\n' +
		'        <th>Country Code</th>' + '\n' +
		'        <th>Reports</th>' + '\n' +
		'      </tr>' '\n'
	)
f.close()

#Read IP file and append each IP to IP list
ips = []
ip_file = new_cwd + 'ips.txt'
with open(ip_file, 'r+') as f: 
	file = f.read().split('\n')
	for ip in file:
		if not ip.strip() == '':
			ips.append(ip)
f.close()

#For each IP in IP list, query AbuseIPDB Check API Endpoint and print results to reports file, then append the information in HTML to the HTML file
for ip in ips:  
	url = 'https://api.abuseipdb.com/api/v2/check'
	report_url = 'https://abuseipdb.com/check/' + str(ip)
	headers = {
		'Accept': 'application/json',
		'key': '{}'.format(os.environ['abuseipdbkey'])
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
			'AbuseIPDB Report: ' + report_url + '\n' +
			'VirusTotal Report: ' +  "https://www.virustotal.com/gui/ip-address/{}".format(str(ip)) + '\n' +
			'IP Teoh Report: ' + "https://ip.teoh.io/{}".format(str(ip))
			+ ('\n' * 3) 
			)
	f.close()
	with open(html_file, 'a') as h: 
		h.write(
			'      <tr>' + '\n' +
			'        <td>{}</td>'.format(str(ip)) + '\n'
			)
		h.close()
	if response['data']['abuseConfidenceScore'] >= 50:
		with open(html_file, 'a') as h:
			h.write(
				'        <td style="color:red">{}</td>'.format(str(response['data']['abuseConfidenceScore'])) + '\n'
				)
		h.close()
	elif response['data']['abuseConfidenceScore'] >= 25 and response['data']['abuseConfidenceScore'] <= 49:
		with open(html_file, 'a') as h:
			h.write(
				'        <td style="color:orange">{}</td>'.format(str(response['data']['abuseConfidenceScore'])) + '\n'
				)
		h.close()
	else:
		with open(html_file, 'a') as h:
			h.write(
				'        <td>{}</td>'.format(str(response['data']['abuseConfidenceScore'])) + '\n'
				)
		h.close()
	with open(html_file, 'a') as h:
		h.write(
			'        <td>{}</td>'.format(str(response['data']['domain'])) + '\n' +
			'        <td>{}</td>'.format(str(response['data']['countryCode'])) + '\n' +
			'        <td><a href="{}">1</a> <a href="https://www.virustotal.com/gui/ip-address/{}">2</a> <a href="https://ip.teoh.io/{}">3</a></td>'.format(report_url, str(ip), str(ip)) + '\n' +
			'      </tr>' + '\n'
			)
	h.close()

#Finish off the HTML file
with open(html_file, 'a') as h: 
	h.write(
		'    </table>' + '\n' +
  		'  </body>' + '\n' +
		'</html>'
	)
h.close()

#Open HTML file on a new tab in the default browser
webbrowser.open_new_tab(html_file)

#EzLife
