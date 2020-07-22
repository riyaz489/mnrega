#!/usr/bin/env python3
"""Personal Website Safe and Block List Management Script"""
import os
import sys
from pprint import pprint
from subprocess import call

import hug
from tldextract import extract

from allow import config


@hug.cli(output=pprint)
def allow(*websites):
    """Mark a website as safe adding it to the safelist. Must be ran as root or using sudo.

       Running without andy websites will list the currently allowed sites
       Running with "init" as the the only argument will pull init using the current vetted domain list.
    """
    if websites == ("init", ):
        add_to_allowed_websites = config.SAFE_LIST
    else:
        add_to_allowed_websites = set()
        for website in websites:
            try:
                extracted = extract(website)
                add_to_allowed_websites.add(f"{extracted.domain}.{extracted.suffix}")
            except Exception:
                raise ValueError(f"Unable to parse given domain: {website}")

    whitelisted = set()
    with open(config.DNS_MASQ, 'r') as allowed:
        for line in allowed:
            if line.startswith("server=/") and line.endswith("/8.8.8.8\n"):
                whitelisted.add(line.replace("server=/", "", 1).replace("/8.8.8.8\n", "", 1))
    if not add_to_allowed_websites:
        return whitelisted

    already_whitelisted = whitelisted.intersection(add_to_allowed_websites)
    if already_whitelisted:
        sys.exit(f"ERROR: Aborting as some of the specified sites are already whitelisted {already_whitelisted}")

    if not os.geteuid() == 0:
        return call(['sudo', 'python3', *sys.argv])

    with open(config.DNS_MASQ, 'a') as whitelist:
        for website in add_to_allowed_websites:
            whitelist.write(f"server=/{website}/8.8.8.8\n")

    call(('/etc/init.d/dnsmasq', 'restart'))
