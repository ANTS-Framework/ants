"""inventory
=============

Utility functions for inventory scripts.
"""

import os
import json
import socket


def get_hostname():
    """Return FQDN for this host in lower case."""
    return socket.gethostname().lower()


def get_simple_hostname(fqdn):
    """Convert FQDN and return simple host name."""
    simple_hostname = fqdn.split('.')[0]
    return simple_hostname


def format_output(output):
    """Return results in Ansible JSON syntax.

    Ansible requirements are documented here:
    http://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html
    """
    return json.dumps(output, sort_keys=True, indent=4, separators=(',', ': '))


def write_cache(cache_file, output):
    """Format and write inventory cache to file."""
    with open(cache_file, 'w') as cache:
        for line in format_output(output):
            cache.write(line)


def read_cache(cache_file):
    """Read cache file and return content or False."""
    if not os.path.isfile(cache_file):
        return False
    with open(cache_file, 'r') as cache:
        return cache.read()


if __name__ == '__main__':
    pass
