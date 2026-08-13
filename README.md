402 - Payment required
======================

[![Super-Linter](https://github.com/suhancz/402/actions/workflows/linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

Generate HTML CV (with an HTTP response code of `402 - Payment required` ;)) from Markdown and add client IP as a [subaddress](https://en.wikipedia.org/wiki/Email_address#Sub-addressing) to my email address so I now from where they really contact me without having to check my mailserver logs.

The script parses the `Accept-Language` HTTP header and tries to respond in the browser's preferred language. This is done by file suffixes, meaning, if one sets their CV in a default language (`402.md`), but also can have the same specified for US English (`402.en-US.md`), Czech (`402.cs.md`), and Hungarian (`402.hu.md`), just by creating the Markdown following the [language or locale code](https://simplelocalize.io/data/locales/) in the filename.

The script also generates a PDF file out of the HTML content to allow providing it in its static form. The PDF is saved with the same filename as the Markdown, but with the extension `.{subaddress}.pdf` in the same directory as the script is hosted.

---
**IMPORTANT**

The script depends on [WKHTMLtoPDF](https://wkhtmltopdf.org) - please, install it on your server if you didn't do it so

---

X server hack
-------------

For having all [WKHTMLtoPDF](https://wkhtmltopdf.org)'s features, one need to run it inside an X server. In my case, on AlmaLinux 8 the exact [steps provided for Amazon Linux](https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server#amazon-linux-2) won't work as [WKHTMLtoPDF](https://wkhtmltopdf.org) is deployed as `/usr/local/bin/wkhtmltopdf` by the package, so I rather run the whole script in Xvfb

SystemD service example
-----------------------

```less
# /etc/systemd/system/402.service
[Unit]
Description=402, serve my CV in Markdown
After=network.target

[Service]
ExecStart=xvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/local/bin/402.py
Environment=CV=/etc/402/402.md
Environment=HOSTNAME=402.balla.cloud
Environment=PORT=402
Environment=DNS=8.8.8.8
Environment='CSS=<link rel="stylesheet" href="https://unpkg.com/terminal.css" /><body class="terminal">'
Environment='PDFCSS=<meta http-equiv="Content-type" content="text/html; charset=utf-8" /><meta charset="utf-8"><style>:global {font-size: 7px !important; line-height: 100%; font-family: "monospace" !important;}* {font-size: 7px !important; line-height: 100%; font-family: "monospace" !important;}:root {--global-font-size: 7px; --global-line-height: 100%; --global-font-family: "monospace";}</style>'

[Install]
WantedBy=multi-user.target
```

Apache config example
---------------------

```apache
<IfModule mod_ssl.c>
SSLStaplingCache shmcb:/var/run/apache2/stapling_cache(128000)
<VirtualHost *:443>
  ServerName 402.balla.cloud

  DocumentRoot /var/www/402/

  ErrorLog /var/log/httpd/402_error.log
  CustomLog /var/log/httpd/402_access.log combined

Header set Status "HTTP/1.1 402 Payment required"
ProxyPass / http://127.0.0.1:402/
ProxyPassReverse / http://127.0.0.1:402/

SSLCertificateFile /etc/letsencrypt/certificates/balla.cloud.pem
SSLCertificateKeyFile /etc/letsencrypt/certificates/balla.cloud.key
Include /etc/letsencrypt/options-ssl-apache.conf
Header always set Strict-Transport-Security "max-age=31536000"
SSLUseStapling on
</VirtualHost>
</IfModule>
```

Input example
-------------

I formatted the below Markdown input to be YAML-parsable, because why not (linter exceptions are added to fit the YAML scheme)

```markdown
# --- # 402 - Payment required - i.e. Curriculum Vitae

## Personal_Information:

-&nbsp;`Name`: Ákos Péter BALLA

-&nbsp;`Telephone`: [+3670.*sha8](tel:+3670.*sha8)

-&nbsp;`Internet`:

&nbsp;&nbsp;-&nbsp;`Email`: <noreply@balla.cloud>

&nbsp;&nbsp;-&nbsp;`WWW`: <https://402.balla.cloud>

&nbsp;&nbsp;-&nbsp;`LinkedIn`: <https://www.linkedin.com/in/akosballa>

&nbsp;&nbsp;-&nbsp;`GitHub`: <https://github.com/suhancz>

## Relevant_expertise:

### &nbsp;&nbsp;Comfortable_with:
&nbsp;&nbsp;&nbsp;&nbsp;[Ansible, cloud-init, Docker, GitHub_Actions, GitLab_CI, Jenkins, Linux, Prometheus, PowerShell, Python, Solaris, TeamCity, Terraform, Windows_server]

### &nbsp;&nbsp;Also_experienced_with:
&nbsp;&nbsp;&nbsp;&nbsp;[AIX, AWS, Azure, Bamboo, BlueCoat, Chef, Cisco_ASA, Cisco_CSS, F5_BigIP, HP-UX, InSpec, k3s, k8s, IBM_cloud, Juniper, Microsoft_BizTalk, Microsoft_SQL_server, Octopus_Deploy, OpenStack, SiteMinder]

## Relevant_professional_experience:

### &nbsp;&nbsp;-&nbsp;Thermo Fisher Scientific:

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Time`: 2022-01-01 - nowadays

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`URL`: <https://thermofisher.com>

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Role`: Software Engineer III

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Main_achievements`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Implemented LDAP-based authorization with authentication using GitLab SSH keys on Linux systems without joining them to the corporate Active Directory

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Improved platform observability and alert accuracy by switching to the Prometheus/Thanos/Loki/Grafana stack

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Secured developer workflows by deploying K8s-based automated code-signing Linux+Windows clusters

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`What_I_learnt`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`10_layers_of_OSI`: Ian Farquhar of RSA proposed something useful

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Yak_shaving`: Distractions are sometimes very important

### &nbsp;&nbsp;-&nbsp;Wandera (a Jamf company):

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Time`: 2020-10-05 - 2021-09-30

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`URL`: <https://wandera.com>

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Role`: Operations Engineer

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Main_achievements`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Accelerated global scale-out by scripting and deploying virtual datacenters across multiple cloud providers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Standardized the global infrastructure stack by migrating the entire codebase to Terraform 0.13

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`What_I_learnt`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Tech`: Gained hands-on experience with diverse cloud providers and widened Terraform knowledge

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Acquisitions`: When an employer is purchased, rules might change a lot

### &nbsp;&nbsp;-&nbsp;Blackboard:

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Time`: 2015-05-04 - 2019-08-31

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`URL`: <https://blackboard.com>

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Role`: DevOps Engineer

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Main_achievements`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Maintained 100% uptime during a full team replacement by reverse-engineering and documenting the entire SaaS environment, and finding the right talent for the job

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Reduced security risks by building a product-independent DDoS protection solution that automatically blocked suspicious traffic

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Migrated legacy products (Connect, Parentlink) from self-hosted infrastructure to AWS to improve reliability

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`What_I_learnt`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Doing_good`: Working for a mission-driven company (education) significantly boosts motivation

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Internal_employment`: I prefer internal roles for better communication on priorities

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`EAFP`: Learnt a vital principle for work efficiency

### &nbsp;&nbsp;-&nbsp;Morgan Stanley:

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Time`: 2008-09-29 - 2012-07-23

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`URL`: <https://ms.com>

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Role`: UNIX L3 Web Infrastructure Engineer

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Main_achievements`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Maintained several packages of the internally developed Linux distribution

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Ensured stability for high-traffic events by preparing web plants for major IPOs (Facebook, GM, NOEnergy)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Contributed to the forensics and recovery effort during the 2009 "Operation Aurora" cyberattack

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Generated an "outage pack" tool which collects all required info on a system in case of issues to ease root cause analysis

&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`What_I_learnt`:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Code_of_conduct`: "Always keep your sense of humor" was the most agreeable requirement I ever signed

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;`Follow_the_Sun`: Global teams make operations much more comfortable

## Education:

### -&nbsp;`Languages`:

&nbsp;&nbsp;-&nbsp;`Czech`: intermediate

&nbsp;&nbsp;-&nbsp;`English`: advanced

&nbsp;&nbsp;-&nbsp;`German`: beginner

&nbsp;&nbsp;-&nbsp;`Hungarian`: native

&nbsp;&nbsp;-&nbsp;`Italian`: beginner

&nbsp;&nbsp;-&nbsp;`Spanish`: beginner

-&nbsp;`Certificates`: [[RHCS in Ansible Automation, RHCE, RHCSA](https://rhtapps.redhat.com/verify?certId=140-113-325)]

-&nbsp;`Gábor Dénes Főiskola`: Information Technology (DNF - chose to work instead)

-&nbsp;`Móricz Zsigmond Technical School`: Computersystems-Programmer (BSc equivalent diploma)

-&nbsp;`Driving_license`: [AM,B1,B,T,K]

## Hobbies_and_interests:

[capoeira, cycling, demoscene, geocaching]
```

External sources
----------------

* [Default style sheet by Jonas D.](https://github.com/Gioni06/terminal.css)
* [TerminessNerdFont-Regular for the PDF by Ryan L McIntyre](https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/Terminus/TerminessNerdFont-Regular.ttf)
* [X server trick taken from python-pdfkit's wiki](https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server)
