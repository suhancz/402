#!/usr/bin/env python3

# Disable all the line-too-long violations in this function
# pylint: disable=line-too-long
# Disable all the invalid-name violations in this function
# pylint: disable=invalid-name

"""_summary_
Generate HTML CV (with a response code of 402 - payment required ;)) from \
    Markdown and add client IP as a tag to my e-mail address so I now from \
    where they really contact me without having to check my mailserver logs
"""

import argparse
import os
import re
from multiprocessing import Process
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import dns.reversename  # type: ignore  # pylint: disable=import-error
import markdown  # pylint: disable=import-error
import pdfkit  # type: ignore  # pylint: disable=import-error
from pypdf import PdfWriter  # type: ignore  # pylint: disable=import-error


class EnvDefault(argparse.Action):  # pylint: disable=too-few-public-methods
    """_summary_
    Get arguments from environment variables
    """

    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(  # pylint: disable=super-with-arguments
            default=default, required=required, **kwargs
        )

    def __call__(
        self, parser, namespace, values, option_string=None
    ):  # pylint: disable=redefined-outer-name
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--cv",
    action=EnvDefault,
    envvar="CV",
    help="Specify the CV markdown path to process (can also be specified \
        using CV environment variable)",
)
parser.add_argument(
    "-hn",
    "--hostname",
    action=EnvDefault,
    envvar="HOSTNAME",
    help="Specify the hostname to serve the page on (can also be specified \
        using HOSTNAME environment variable)",
)
parser.add_argument(
    "-p",
    "--port",
    action=EnvDefault,
    envvar="PORT",
    help="Specify the port to serve the page on (can also be specified using \
        PORT environment variable)",
)
parser.add_argument(
    "-d",
    "--dns",
    action=EnvDefault,
    envvar="DNS",
    required=False,
    help="Specify the DNS server to look up remote addresses via (can also be \
        specified using DNS environment variable)",
)
parser.add_argument(
    "-sa",
    "--subaddress",
    action=EnvDefault,
    envvar="SUBADDRESS",
    required=False,
    help="Specify the sub-address (the part in the e-mail after the '+' sign) \
        to use for incoming e-mails (can also be specified using SUBADDRESS \
        environment variable, or passed as the subaddress HTTP parameter)",
)
parser.add_argument(
    "-s",
    "--style",
    action=EnvDefault,
    envvar="CSS",
    required=False,
    help="Specify the CSS including the <style> or <link> tags for the output \
        HTML",
    default='<link rel="stylesheet" \
        href="https://unpkg.com/terminal.css@0.7.4/dist/terminal.min.css" />\
        <body class="terminal">',
)
args = parser.parse_args()


def parseAcceptLanguage(acceptLanguage):
    """_summary_

    Args:
        acceptLanguage (string): Parse Accept-Language HTTP header

    Returns:
        list: sorted tuples of language codes and weigths
    """
    languages = acceptLanguage.split(",")
    locale_q_pairs = []

    for language in languages:
        if language.split(";")[0] == language:
            # no q => q = 1
            locale_q_pairs.append((language.strip(), "1"))
        else:
            locale = language.split(";")[0].strip()
            q = language.split(";")[1].split("=")[1]
            locale_q_pairs.append((locale, q))
    return sorted(locale_q_pairs, key=lambda x: x[1], reverse=True)


def generatepdf(html, subaddress, filename):
    """_summary_
    generate PDF from content

    Args:
        html (string): HTML content to convert to PDF
        subaddress (string): subaddress to generate the file name from
        filename (string): original Markdown filename
    """
    pdf_options = {"encoding": "UTF-8", "page-size": "A4"}
    pdf_file = filename.replace(".md", f".{subaddress}.pdf")
    pdfkit.from_string(html, pdf_file, options=pdf_options)
    writer = PdfWriter(clone_from=pdf_file)
    writer.create_viewer_preferences()
    writer.add_metadata(
        {
            "/Author": "Akos Balla <402+pdf@balla.cloud>",
            "/Title": "402 - Payment required",
        }
    )
    writer.viewer_preferences.center_window = True
    writer.viewer_preferences.hide_toolbar = True
    writer.viewer_preferences.hide_menubar = True
    writer.viewer_preferences.hide_windowui = True
    writer.viewer_preferences.display_doctitle = True
    with open(pdf_file, "wb") as f:
        writer.write(f)


class SimpleServer(BaseHTTPRequestHandler):
    """_summary_
    Web server doing the heavy lifting
    """

    def do_GET(self):
        """_summary_
        respond on GET requests
        """
        query_string = parse_qs(urlparse(self.path).query)
        if query_string:
            subaddress = query_string["subaddress"][0]
        elif args.subaddress:
            subaddress = args.subaddress
        else:
            ip_forward = self.headers.get("X-Forwarded-For")
            if ip_forward:
                ip = ip_forward.split(",")[0]
                print("returning forwarded for ip address", ip)
            elif self.headers.get("X-Real-IP"):
                ip = self.headers.get("X-Real-IP")
                print("returning REAL_IP ", ip)
            else:
                ip = self.client_address[0]
                print("returning remote address ", ip)
            subaddress = dns.reversename.from_address(ip)
        filename = args.cv
        for language in parseAcceptLanguage(self.headers["Accept-Language"]):
            file_suffix = language[0]
            filename = args.cv
            cv_array = filename.split(".")
            cv_array.insert(-1, file_suffix)
            filename = ".".join(cv_array)
            if not os.path.isfile(filename):
                filename = args.cv
            else:
                print("found localized file", filename)
                break
        with open(filename, encoding="utf-8") as f:
            text = f.read()
            html = args.style + markdown.markdown(
                re.sub(
                    r"(<)([A-Za-z0-9._%+-]+)(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})(>)",
                    rf"[\2\3](mailto:\2+{subaddress}\3)",
                    text,
                )
            )
        p = Process(target=generatepdf, args=(html, subaddress, filename))
        p.daemon = True
        p.start()
        self.send_response(402)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("X-Robots-Tag", "noindex")
        self.end_headers()
        self.wfile.write(bytes(html, encoding="utf8"))


if __name__ == "__main__":
    webServer = HTTPServer((args.hostname, int(args.port)), SimpleServer)
    print("Server started http://{args.hostname}:{args.port}")
try:
    webServer.serve_forever()  # pylint: disable=used-before-assignment
except KeyboardInterrupt:
    pass
webServer.server_close()
print("Server stopped.")
