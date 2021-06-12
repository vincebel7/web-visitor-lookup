import re, requests, json

logfile = "/var/log/apache2/access.log"
search_string = "GET / HTTP"
ip_regex = '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'

def is_valid_addr(s):
    if re.match(ip_regex, s): return True
    return False

def lookup_location(ip_addr):
    if not is_valid_addr(ip_addr):
        print("Error: Invalid IP address ", ip_addr)
        return
    
    host = "https://freegeoip.app/json/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
    }

    url = host + ip_addr

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)

    country = data["country_name"]
    if(country == "United States"):
        state = data["region_name"]
        city = data["city"]
        print(" [ " + ip_addr + " ] " + city + ", " + state)

    return

def read_file(f):
    file = open(f, 'r')
    Lines = file.readlines()

    for line in Lines:
        if(search_string in line):
            addr = re.search(ip_regex, line)
            lookup_location(addr.group())

read_file(logfile)
