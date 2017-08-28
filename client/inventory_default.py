#!/usr/bin/python

"""inventory_default
===================


Default inventory script.

This is a dummy inventory script to bootstrap ants.
It will return localhost and fqdn as members of
the ants-common group.

These values can be used to assign roles in local.yml but
using a dynamic inventory script like inventory_ad.py
is the prefered way of running ants.
"""

from antslib import inventory


def main():
    """Print default inventory in JSON."""
    output = dict()
    fqdn = inventory.get_hostname()
    output['ants-common'] = (fqdn)
    print inventory.format_output(output)


if __name__ == '__main__':
    main()
