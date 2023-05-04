# IPDb2Txt
A simplen Python 3 script that iterates through IPs and queries them via AbuseIPDB Check Endpoint API. This script will also generate an HTML document that will automatically open in a new tab in your default browser once the script completes.

## Setup
- Create an AbuseIPDB account and get an API key
- Create an environment variable called "abuseipdbkey" and set the value to your AbuseIPDB API key
- Create a text file called "ips.txt" in the same directory as the script and put each IP that you want to check on a new line

## Usage 
    python3 IPInfoFromTxt.py
