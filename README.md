# Gandi DDNS

This is a simple script for updating a DNS record in a zone hosted at Gandi (in LiveDNS) to match the current public IP 
address of the system on which it's run.

## Installation

Checkout the GIT repository to a suitable directory, and then create a Python virtual environment:

```shell
cd /usr/local
git clone https://github.com/dpage/gandi-ddns.git
cd gandi-ddns
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

You will need a Gandi API key. To get that (correct as of January 5th 2024):

1) Login to Gandi
2) Click your account name in the header, and select *User Settings*.
3) Click the *View my Personal Access Tokens* button.
4) Click the *Create a token* button.
5) Select the appropriate organisation and click *Next*.
6) Enter a token name, and select the expiry period.
7) Under *Token resources*, select *Restrict to selected products*.
8) Select the domain name.
9) Enable the options for *Manage domain name technical configurations* and *See and renew domain names*.
10) Click *Create*.

You will be shown the token but only once, so make sure you make a note of it!

Now make a copy of *config.json.in* and call it *config.json*. Edit *config.json*, and set the hostname, domain, and
API key. You can also change the TTL for the DNS record if required.

Note: You should secure the configuration file against prying eyes, for example:
```shell
chmod 600 config.json
```  

## Running

Simply run the script under the Python virtual environment, for example:
```shell
/usr/local/gandi-ddns/venv/bin/python3 /usr/local/gandi-ddns/gandi-ddns.py 
2024-01-05 11:17:30.702259: Checking: ddns.example.com
    Current IP: 10.1.2.3
    DNS IP:     
    Updating DNS records at Gandi...
    DNS updated.
```

It may take a minute or two for Gandi's public facing DNS servers to catch up. Once they have, run the script again (it 
won't hurt to do it earlier - it'll just try to re-create/update the record again):
```shell
/usr/local/gandi-ddns/venv/bin/python3 /usr/local/gandi-ddns/gandi-ddns.py 
2024-01-05 11:20:57.022458: Checking: ddns.example.com
    Current IP: 10.1.2.3
    DNS IP:     10.1.2.3
    No IP address change detected.
```

Note that if the API key is incorrect or other errors occur, you will see output similar to:
```shell
2024-01-05 11:21:50.492538: Checking: Checking: ddns.example.com
    Current IP: 10.1.2.3
    DNS IP:     
    Updating DNS records at Gandi...
    Unexpected response updating DNS at Gandi: 500 - The server has either erred or is incapable of performing the requested operation.
```

Check that everything looks good in your zone in the LiveDNS web interface, and assuming it is, setup a cron job to 
run the script every minute or so.
