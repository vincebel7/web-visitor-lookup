# web-visitor-lookup
# Author: https://github.com/vincebel7

import re, requests, json, gzip
ip_regex = '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'

# -------------
# Configuration
# -------------

# Directory where logfiles exist
log_dir = "/var/log/apache2/"

# Most recent logfile
logfile = log_dir + "access.log"

# How many logfiles are kept
logrotate_count = 13

# Search string. Default is "GET / HTTP" to search only for homepage hits
search_string = "GET / HTTP"

# Location API. Options are: ipapi (45 requests/min), ipwhois (1000 requests/day)
location_api = "ipwhois"

def is_valid_addr(s):
    if re.match(ip_regex, s): return True
    return False

def lookup_location(ip_addr):
    if(location_api == "ipwhois"): lookup_location_ipwhois(ip_addr)
    elif(location_api == "ipapi"): lookup_location_ipapi(ip_addr)
    else: print("Invalid API")

def lookup_location_ipapi(ip_addr): # 45/min
    if not is_valid_addr(ip_addr):
        print("Error: Invalid IP address ", ip_addr)
        return
    
    host = "http://ip-api.com/json/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    url = host + ip_addr
    response = requests.request("GET", url, headers=headers)
    if(response.status_code != 200):
        return
    data = json.loads(response.text)

    if(data["countryCode"]):
        country = data["countryCode"]
        if(country == "US"):
            state = data["regionName"]
            city = data["city"]
            print(" [ " + ip_addr + " ] " + city + ", " + state)

def lookup_location_ipwhois(ip_addr): # 1000/day
    if not is_valid_addr(ip_addr):
        print("Error: Invalid IP address ", ip_addr)
        return
    
    host = "http://ipwhois.app/json/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    url = host + ip_addr
    response = requests.request("GET", url, headers=headers)
    if(response.status_code != 200):
        print("HTTP error " + str(response.status_code))
        return
    data = json.loads(response.text)

    if(data["country_code"]):
        country = data["country_code"]
        if(country == "US"):
            state = data["region"]
            city = data["city"]
            print(" [ " + ip_addr + " ] " + city + ", " + state)

def read_file(f):
    file = open(f, 'r')
    Lines = file.readlines()

    for line in Lines:
        if(search_string in line):
            addr = re.search(ip_regex, line)
            lookup_location(addr.group())

def gzip_open(i): # unzip .gz to new file, return unzipped filename
    unzipped = logfile + "." + str(i)
    zipped = unzipped + ".gz"

    f = gzip.open(zipped, 'r')
    data = f.read()
    datastr = data.decode()
    with open(unzipped,"w") as f:
        f.write(datastr)

    return unzipped
 
print("Using API: " + location_api)
read_file(logfile)
read_file(logfile + ".1")
for i in range(2,logrotate_count): # apache compresses logs after most recent two
    read_file(gzip_open(i))
