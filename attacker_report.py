#!/usr/bin/env python3
# Student: Adam Levin
# Current Date: 04/022/2026
# Due Date: 04/24/2026
# Class: NSSA 221 Section 03
# Assignement: Script 4

import re
import os
import builtins
from datetime import datetime
from collections import defaultdict
from geoip import geolite2

# Fix for Python 3.13 compatibility: python-geoip-geolite2 opens the .mmdb
# database in text mode instead of binary mode, causing a TypeError. Patching
# the built-in open() to force binary mode for .mmdb files resolves this.
_real_open = open
def _binary_open(filename, mode="r", **kwargs):
    if isinstance(filename, str) and filename.endswith(".mmdb"):
        mode = "rb"
        kwargs.pop("encoding", None)
        kwargs.pop("errors", None)
    return _real_open(filename, mode, **kwargs)
builtins.open = _binary_open

# path to the syslog file and minimum failed attempts to appear in the report
LOG_FILE = "/home/student/syslog.log"
THRESHOLD = 10

# clear the terminal before displaying the report
def clear_terminal():
    os.system("clear")

# parse the log file and return IPs with failed login counts at or above the threshold
def parse_failed_logins(log_file):
    ip_counts = defaultdict(int)

    # regex to match failed SSH login lines and capture the source IP address
    pattern = re.compile(r"Failed password for .+ from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

    with open(log_file, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                ip_counts[match.group(1)] += 1

    # filter out any IPs that don't meet the minimum attempt threshold
    return {ip: count for ip, count in ip_counts.items() if count >= THRESHOLD}

# look up the country code for a given IP address using the GeoLite2 database
def get_country(ip):
    result = geolite2.lookup(ip)
    if result and result.country:
        return result.country
    return "Unknown"

# print the attacker report to the terminal sorted by count in ascending order
def display_report(attackers):
    # sort attackers by attempt count from lowest to highest
    sorted_attackers = sorted(attackers.items(), key=lambda item: item[1])

    # ANSI color codes for terminal output
    GREEN = "\033[92m"
    RED   = "\033[91m"
    RESET = "\033[0m"

    # print the report title with the current date
    current_date = datetime.now().strftime("%B %d, %Y")
    print(f"{GREEN}Attacker Report{RESET} - {current_date}\n")

    # print column headers
    print(f"{RED}{'COUNT':<10}{'IP ADDRESS':<18}{'COUNTRY'}{RESET}")

    # print one row per offending IP with its country of origin
    for ip, count in sorted_attackers:
        country = get_country(ip)
        print(f"{count:<10}{ip:<18}{country}")

    print()

# main function to validate the log file, parse it, and display the report
def main():
    clear_terminal()

    # exit early if the log file doesn't exist
    if not os.path.isfile(LOG_FILE):
        print(f"Error: Log file not found at '{LOG_FILE}'")
        return

    attackers = parse_failed_logins(LOG_FILE)

    # exit early if no IPs exceeded the threshold
    if not attackers:
        print(f"No IP addresses found with {THRESHOLD} or more failed login attempts.")
        return

    display_report(attackers)

if __name__ == "__main__":
    main()