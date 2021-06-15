# web-visitor-lookup
Author: https://github.com/vincebel7

Prints locations of website visitors by scraping access logs.
Supports two different location APIs, depending on if you find 45 requests/min or 1000 requests/day more useful.

This is just for fun, and I'm sure could be optimized in a million different ways.

NOTE: The user that runs visitors.py must have rwx permissions on the logfile directory.

This program was written and tested using Python 3.6.9.

### How to use
```
git clone https://github.com/vincebel7/web-visitor-lookup

python3 web-visitor-lookup/lookup.py
```

The program will search through access logs and print out the city and state of website visitors.

### Configuration help
Configured by default for Apache on Ubuntu, filtering to US visitors only. Tweak the configuration section at the top of lookup.py for different systems or setups.
Other web servers have not been tested, but it should be the same concept if you change the log directory and logfile name.

**log_dir** - The directory where logfiles are kept. For Apache on Ubuntu, this should be `/var/log/apache2/`

**logfile** - The full path of the most recent logfile. This program assumes the logfile rotation follows the pattern: `logfile.1`, `logfile.2`, etc.

**logrotate_count** - The number of logfiles the program should check through. This number should not exceed what is configured in your system's logrotate file. For Apache on Ubuntu this is found in `/etc/logrotate.d/apache2`

**search_string** - Search string. Default is "GET / HTTP" to search only for homepage hits, can shorten to "GET /" to search all page hits

**location_api** - The location API to use. Options are: ipapi (45 requests/min), ipwhois (1000 requests/day)
