#!/usr/bin/env python3

# Disable all the line-too-long violations in this function
# pylint: disable=line-too-long
# Disable all the invalid-name violations in this function
# pylint: disable=invalid-name

"""_summary_
Generate HTML CV (with a response code of 402 - payment required ;)) from Markdown and add client IP as a tag to my e-mail address so I now from where they really contact me without having to check my mailserver logs
"""

import argparse
import os
import re
from http.server import SimpleHTTPRequestHandler, HTTPServer
import markdown
import dns.reversename
# from bs4 import BeautifulSoup as Soup

class EnvDefault(argparse.Action): # pylint: disable=too-few-public-methods
    """_summary_
    Get arguments from environment variables
    """
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, # pylint: disable=super-with-arguments
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None): # pylint: disable=redefined-outer-name
        setattr(namespace, self.dest, values)

parser=argparse.ArgumentParser()
parser.add_argument(
    "-c", "--cv", action=EnvDefault, envvar='CV',
    help="Specify the CV markdown path to process (can also be specified using CV environment variable)")
parser.add_argument(
    "-hn", "--hostname", action=EnvDefault, envvar='HOSTNAME',
    help="Specify the hostname to serve the page on (can also be specified using HOSTNAME environment variable)")
parser.add_argument(
    "-p", "--port", action=EnvDefault, envvar='PORT',
    help="Specify the port to serve the page on (can also be specified using PORT environment variable)")
parser.add_argument(
    "-d", "--dns", action=EnvDefault, envvar='DNS', required=False,
    help="Specify the DNS server to look up remote addresses via (can also be specified using DNS environment variable)")
parser.add_argument(
    "-a", "--subaddress", action=EnvDefault, envvar='SUBADDRESS', required=False,
    help="Specify the sub-address (the part in the e-mail after the '+' sign) to use for incoming e-mails (can also be specified using SUBADDRESS environment variable)")
parser.add_argument(
    "-s", "--style", action=EnvDefault, envvar='CSS', required=False,
    help="Specify the CSS including the <style> or <link> tags for the output HTML", default='<link rel="stylesheet" href="https://unpkg.com/terminal.css@0.7.4/dist/terminal.min.css" /><body class="terminal">')
args=parser.parse_args()

class SimpleServer(SimpleHTTPRequestHandler):
    """_summary_
    Web server doing the heavy lifting
    """
    def do_GET(self):
        if args.subaddress:
            subaddress = args.subaddress
        else:
            ip_forward = self.headers.get("X-Forwarded-For")
            if ip_forward:
                ip = ip_forward.split(",")[0]
                print("returning forwarded for ip address", ip)
            elif self.headers.get("X-Real-IP"):
                ip = self.headers.get("X-Real-IP")
                print ("returning REAL_IP ", ip)
            else:
                ip = self.client_address[0]
                print("returning remote address ", ip)
            subaddress = dns.reversename.from_address(ip)
        with open(args.cv, encoding='utf-8') as f:
            text = f.read()
            html = args.style + markdown.markdown(re.sub(r'(<)([A-Za-z0-9._%+-]+)(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})(>)', rf'[\2\3](mailto:\2+{subaddress}\3)', text))
        self.extensions_map = {k: v + ';charset=UTF-8' for k, v in self.extensions_map.items()}
        self.send_response(402)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("X-Robots-Tag", "noindex")
        self.end_headers()
        self.wfile.write(bytes(html, encoding='utf8'))

if __name__ == "__main__":
    webServer = HTTPServer((args.hostname, int(args.port)), SimpleServer)
    print("Server started http://{args.hostname}:{args.port}")
try:
    webServer.serve_forever() # pylint: disable=used-before-assignment
except KeyboardInterrupt:
    pass
webServer.server_close()
print("Server stopped.")
