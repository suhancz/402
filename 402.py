#!/usr/bin/env python3

# Disable all the line-too-long violations in this function
# pylint: disable=line-too-long
# Disable all the invalid-name violations in this function
# pylint: disable=invalid-name

"""_summary_
Generate HTML CV (with a response code of 402 - payment required ;)) from \
    Markdown and add client IP as a tag to my e-mail address so I now from \
    where they really contact me without having to check my mailserver logs

Input Markdown format
---------------------
Write a normal Markdown file using standard heading levels (# through ######)
and standard list items (- item).  The script converts the heading/list
hierarchy into the NBSP-indented YAML-like representation that was previously
maintained by hand, so you no longer need to sprinkle &nbsp; throughout the
source file.

Mapping rules
~~~~~~~~~~~~~
* A heading at level N becomes a list-item at YAML depth (N-1), i.e. the
  ``#`` document-title stays as-is, ``##`` section keys get depth 0,
  ``###`` sub-section keys get depth 1, and so on.
* Plain ``- item`` lines inside a heading section are rendered one level
  deeper than that heading's depth.
* Blank lines and lines that are already rendered with &nbsp; (legacy files)
  are preserved without modification.
"""

import argparse
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import dns.reversename  # type: ignore  # pylint: disable=import-error
import markdown  # pylint: disable=import-error
import pdfkit  # type: ignore  # pylint: disable=import-error
from pypdf import PdfWriter  # type: ignore  # pylint: disable=import-error


# ---------------------------------------------------------------------------
# Pure-Markdown → YAML-like conversion
# ---------------------------------------------------------------------------

def _yaml_indent(depth: int) -> str:
    """Return the NBSP-based indentation string for *depth* (0-indexed)."""
    # depth 0  → ""           (top-level, no leading spaces)
    # depth 1  → "&nbsp;&nbsp;"
    # depth 2  → "&nbsp;&nbsp;&nbsp;&nbsp;"
    # …
    return "&nbsp;&nbsp;" * depth


def md_to_yaml_like(text: str) -> str:  # pylint: disable=too-many-branches
    """Convert a plain Markdown CV into the NBSP-indented YAML-like format.

    The function is idempotent: lines that already contain ``&nbsp;`` are
    passed through unchanged so that the script can still consume legacy
    hand-crafted source files.

    Args:
        text (str): Raw Markdown source.

    Returns:
        str: Markdown source with headings and list-items reformatted to use
             the project's NBSP indentation convention.
    """
    # Heading pattern: optional leading spaces, then one or more '#', then text
    heading_re = re.compile(r"^(#{1,6})\s+(.*)")
    # List-item pattern: optional leading spaces/nbsp, then "- " and text
    list_re = re.compile(r"^\s*-\s+(.*)")

    out_lines: list[str] = []
    # Track the depth of the most-recently-seen heading so that plain list
    # items can be placed one level below it.
    current_heading_depth = 0

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # Pass legacy lines (already contain &nbsp;) straight through
        if "&nbsp;" in line:
            out_lines.append(line)
            continue

        # Blank lines pass through
        if not line.strip():
            out_lines.append(line)
            continue

        heading_match = heading_re.match(line)
        if heading_match:
            hashes, content = heading_match.group(1), heading_match.group(2)
            level = len(hashes)           # 1..6
            depth = level - 1             # 0..5  (h1 → depth 0 = no indent)
            current_heading_depth = depth

            indent = _yaml_indent(depth)

            if depth == 0:
                # The document title (# …) stays as a plain heading
                out_lines.append(f"{'#' * level} {content}")
            else:
                # Sub-headings become YAML-like list-item headings:
                #   ### -&nbsp;Section_Key:
                # We keep the same number of '#' so Markdown renders them as
                # the correct heading level (which produces the right HTML
                # element for the terminal.css styling).
                out_lines.append(f"{'#' * level} {indent}-&nbsp;{content}")
            continue

        list_match = list_re.match(line)
        if list_match:
            content = list_match.group(1)
            # List items sit one level below their parent heading
            depth = current_heading_depth + 1
            indent = _yaml_indent(depth)
            out_lines.append(f"{indent}-&nbsp;{content}")
            continue

        # Everything else (paragraphs, fenced code blocks, etc.) passes through
        out_lines.append(line)

    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

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
    "-l",
    "--language",
    required=False,
    help="Specify the language the output should apperar in (can also be \
        passed as the language HTTP parameter)",
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
        href="https://unpkg.com/terminal.css" />\
        <body class="terminal">',
)
parser.add_argument(
    "-ps",
    "--pdfstyle",
    action=EnvDefault,
    envvar="PDFCSS",
    required=False,
    help='Specify the CSS including the <style> or <link> tags for the output \
        PDF (as WKHTMLtoPDF does not support remote links, one might need it \
        for "local" styling). This value overrides the default CSS, but \
        takes its value if not set',
)
args = parser.parse_args()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

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


def generatePDF(content, pdf_file):
    """_summary_
    Args:
        content (string): HTML content
        pdf_file (string): path to the PDF file
    """
    pdf_options = {
        "encoding": "UTF-8",
        "page-size": "A4",
        "user-style-sheet": "https://unpkg.com/terminal.css",
        "use-xserver": None,
        "no-stop-slow-scripts": None,
        "disable-smart-shrinking": None,
    }
    if os.path.isfile(pdf_file):
        os.remove(pdf_file)
    if "pdfstyle" in args and args.pdfstyle:
        pdf_style = args.pdfstyle
    else:
        pdf_style = args.style
    pdfkit.from_string(
        pdf_style + content,
        pdf_file,
        options=pdf_options,
    )
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


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------

class SimpleServer(BaseHTTPRequestHandler):
    """_summary_
    Web server doing the heavy lifting
    """

    def do_GET(self):  # pylint: disable=too-many-branches,too-many-statements
        """_summary_
        respond on GET requests
        """
        query_string = parse_qs(urlparse(self.path).query)
        print(query_string)
        if "subaddress" in query_string:
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
        language = ""
        target_languages = parseAcceptLanguage(self.headers["Accept-Language"])
        if "language" in query_string:
            target_languages.insert(0, (query_string["language"][0], 1))
        elif args.language:
            target_languages.insert(0, (args.language, 1))
        for language in target_languages:
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
        pdf_file = filename.replace(".md", f".{subaddress}.pdf")
        with open(filename, encoding="utf-8") as f:
            # Convert pure Markdown to the NBSP-indented YAML-like format,
            # then substitute the email sub-address, then render to HTML.
            raw_text = f.read() + "</body>"
            yaml_like_text = md_to_yaml_like(raw_text)
            content = markdown.markdown(
                re.sub(
                    r"(<)([A-Za-z0-9._%+-]+)(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})(>)",
                    rf"[\2\3](mailto:\2+{subaddress}\3)",
                    yaml_like_text,
                )
            )
        if self.path.split("?")[0] == f"/{os.path.basename(pdf_file)}":
            generatePDF(content, pdf_file)
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(pdf_file)}"',
            )
            self.send_header("Content-Length", os.path.getsize(pdf_file))
            self.end_headers()
            with open(pdf_file, "rb") as originalpdf:
                self.wfile.write(bytes(originalpdf.read()))
        else:
            self.send_response(402)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("X-Robots-Tag", "noindex")
            self.end_headers()
            self.wfile.write(
                bytes(
                    f'{args.style}<a href="/{os.path.basename(pdf_file)}?subaddress={subaddress}&language={language[0]}">&#x1f5b6;</a>{content}',
                    encoding="utf8",
                )
            )


if __name__ == "__main__":
    webServer = HTTPServer((args.hostname, int(args.port)), SimpleServer)
    print(f"Server started http://{args.hostname}:{args.port}")
try:
    webServer.serve_forever()  # pylint: disable=used-before-assignment
except KeyboardInterrupt:
    pass
webServer.server_close()
print("Server stopped.")
