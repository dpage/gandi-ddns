#!/usr/bin/env python3

import datetime
import json
import os

import dns.resolver
import requests


def load_config():
    """
    Load the app config
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
            c = f.read()
    except FileNotFoundError:
        print('{}: No configuration file found.\n'
              '    Copy config.json.in to config.json and edit as required.'.format(datetime.datetime.now()))
        exit(1)

    return json.loads(c)


def main():
    config = load_config()

    print('{}: Checking: {}.{}'.format(datetime.datetime.now(), config['HOSTNAME'], config['DOMAIN']))

    # Get our current IP
    current_ip = get_current_ip()
    print('    Current IP: {}'.format(current_ip))

    # Get our DNS IP
    dns_ip = get_dns_ip('{}.{}'.format(config['HOSTNAME'], config['DOMAIN']))
    print('    DNS IP:     {}'.format(dns_ip))

    # Bail out if they match
    if current_ip == dns_ip:
        print('    No IP address change detected.')
        exit(0)

    # Update DNS
    print('    Updating DNS records at Gandi...')
    update_dns(config['HOSTNAME'], config['DOMAIN'], current_ip, config['APIKEY'])

    print('    DNS updated.')
    exit(0)


def get_current_ip():
    url = 'http://ip-api.com/json'
    return requests.get(url).json()["query"]


def get_dns_ip(host):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['173.246.100.2']
    try:
        res = str(resolver.resolve(host, 'A')[0])
    except:
        res = ''

    return res


def update_dns(hostname, domain, address, apikey):
    headers = {'Authorization': 'Bearer {}'.format(apikey)}
    url = 'https://api.gandi.net/v5/livedns/domains/{}/records/{}/A'.format(domain, hostname)

    payload = {'rrset_name': hostname,
               'rrset_type': 'A',
               'rrset_ttl': 300,
               'rrset_values': [address]}

    try:
        response = requests.put(url, data=json.dumps(payload), headers=headers)
    except:
        print('    Connection error when updating DNS at Gandi.')
        exit(1)

    if response.status_code != 201:
        print('    Unexpected response updating DNS at Gandi: {} - {}'.format(response.status_code,
                                                                              response.json()['message']))
        exit(1)


if __name__ == '__main__':
    main()
