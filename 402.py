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
hierarchy into the NBSP-indented YAML-like representation automatically.

Indentation mapping
~~~~~~~~~~~~~~~~~~~
Heading level → NBSP pairs before ``-`` → list-item NBSP pairs underneath

  #   (level 1)  document title, rendered verbatim (no list-item wrapper)
  ##  (level 2)  0 NBSP pairs  → list items get 1 NBSP pair  (2 &nbsp;)
  ### (level 3)  1 NBSP pair   → list items get 2 NBSP pairs (4 &nbsp;)
  ####(level 4)  2 NBSP pairs  → list items get 3 NBSP pairs (6 &nbsp;)
  …and so on.

Examples (the original hand-written format from README.md)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ## Personal_Information:          →  ## -&nbsp;Personal_Information:
  - `Name`: Ákos                    →  &nbsp;&nbsp;-&nbsp;`Name`: Ákos

  ### - Internet:                   →  ### &nbsp;&nbsp;-&nbsp;Internet:
  - `Email`: …                      →  &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Email`: …

  #### - Red Hat …:                 →  #### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Red Hat …:
  - `Date`: 2014                    →  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Date`: 2014

Backward-compatibility
~~~~~~~~~~~~~~~~~~~~~~
Lines that already contain ``&nbsp;`` are passed through unchanged, so
existing hand-crafted source files keep working without modification.
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

def _nbsp(pairs: int) -> str:
    """Return *pairs* repetitions of ``&nbsp;&nbsp;`` (i.e. 2*pairs &nbsp;)."""
    return "&nbsp;&nbsp;" * pairs


def md_to_yaml_like(text: str) -> str:  # pylint: disable=too-many-branches
    """Convert a plain Markdown CV into the NBSP-indented YAML-like format.

    Heading level N  →  heading rendered with (N-2) NBSP pairs before ``-``
                        (level 1 / ``#`` is the document title and gets no
                        list-item wrapping at all)
    List items       →  indented with (current_heading_level - 1) NBSP pairs

    The function is idempotent: lines that already contain ``&nbsp;`` are
    passed through unchanged so legacy hand-crafted files still work.

    Args:
        text (str): Raw Markdown source.

    Returns:
        str: Markdown with headings and list-items reformatted to use the
             project's NBSP-indentation convention.
    """
    heading_re = re.compile(r"^(#{1,6})\s+(.*)")
    list_re = re.compile(r"^\s*-\s+(.*)")

    out_lines: list[str] = []
    # Level of the most-recently-seen Markdown heading (1-based, matches '#' count)
    current_heading_level: int = 2  # default: top-level section (##)

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # Legacy lines (already NBSP-formatted) pass through unchanged
        if "&nbsp;" in line:
            out_lines.append(line)
            continue

        # Blank lines pass through
        if not line.strip():
            out_lines.append(line)
            continue

        heading_match = heading_re.match(line)
        if heading_match:
            hashes = heading_match.group(1)
            content = heading_match.group(2)
            level = len(hashes)  # 1 … 6
            current_heading_level = level

            if level == 1:
                # Document title: keep verbatim
                out_lines.append(f"# {content}")
            else:
                # Number of NBSP pairs in front of the "-" marker:
                #   ##   (level 2)  → 0 pairs
                #   ###  (level 3)  → 1 pair
                #   #### (level 4)  → 2 pairs
                #   …
                nbsp_pairs = level - 2
                out_lines.append(
                    f"{'#' * level} {_nbsp(nbsp_pairs)}-&nbsp;{content}"
                )
            continue

        list_match = list_re.match(line)
        if list_match:
            content = list_match.group(1)
            # List items sit one indent level below their parent heading:
            #   under ##   (level 2)  → 1 pair  (2 &nbsp;)
            #   under ###  (level 3)  → 2 pairs (4 &nbsp;)
            #   under #### (level 4)  → 3 pairs (6 &nbsp;)
            nbsp_pairs = current_heading_level - 1
            out_lines.append(f"{_nbsp(nbsp_pairs)}-&nbsp;{content}")
            continue

        # Everything else (paragraphs, code fences, raw HTML …) passes through
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
            # Convert pure Markdown → NBSP-indented YAML-like format,
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
