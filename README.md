# 402 - Payment required

[![Super-Linter](https://github.com/suhancz/402/actions/workflows/linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

Generate HTML CV (with an HTTP response code of `402 - Payment required` ;)) from Markdown and add client IP as a subaddress to my email address so I now from where they really contact me without having to check my mailserver logs

## SystemD service example

```less
# /etc/systemd/system/402.service
[Unit]
Description=402, serve my CV in Markdown
After=network.target

[Service]
ExecStart=/usr/local/bin/402.py
Environment=CV=/etc/402/402.md
Environment=HOSTNAME=402.balla.cloud
Environment=PORT=402
Environment=DNS=8.8.8.8
Environment=CSS=<link rel="stylesheet" href="https://unpkg.com/terminal.css@0.7.4/dist/terminal.min.css" /><body class="terminal">

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/402-refresh.path
[Unit]
Description=Watch /etc/402/402.md for changes

[Path]
PathModified=/etc/402/402.md

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/402-refresh.service
[Unit]
Description=Restart 402
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/systemctl restart 402.service

[Install]
RequiredBy=402-refresh.path
```

## Apache config example

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

## Input example

I formatted the below Markdown input to be YAML-parsable, because why not (linter exceptions are added to fit the YAML scheme)

```markdown
# --- # 402 - Payment required - i.e. Curriculum Vitae

## Personal_Information:

- `Name`: Ákos Péter BALLA
- `Date_of_Birth`: YYYY-MM-DD

### -&nbsp;Postal_address:

&nbsp;&nbsp;- `HU`: 1046. Budapest, Utcanév utca 67.

&nbsp;&nbsp;- `CZ`: 602 00. Brno, Ulice 123/45.

### -&nbsp;Telephone:

&nbsp;&nbsp;- `HU`: [+36.*sha.](tel:+36.*sha.)

&nbsp;&nbsp;- `CZ`: [+420.*864](tel:+420.*864)

### -&nbsp;Internet:

&nbsp;&nbsp;- `Email`: <402@balla.cloud>

&nbsp;&nbsp;- `WWW`: <https://402.balla.cloud>

&nbsp;&nbsp;- `LinkedIn`: <https://www.linkedin.com/in/akosballa>

&nbsp;&nbsp;- `GitHub`: <https://github.com/suhancz>

## Education:

### -&nbsp;Certificates:

#### &nbsp;&nbsp;-&nbsp;Red Hat Certified Specialist in Ansible Automation (EX407):

&nbsp;&nbsp;&nbsp;&nbsp;- `Date`: 2017-09-12

&nbsp;&nbsp;&nbsp;&nbsp;- `ID`: [140-113-325](https://rhtapps.redhat.com/verify?certId=140-113-325)

#### &nbsp;&nbsp;-&nbsp;Red Hat Certified Engineer (EX300):

&nbsp;&nbsp;&nbsp;&nbsp;- `Date`: 2014-09-19

&nbsp;&nbsp;&nbsp;&nbsp;- `ID`: [140-113-325](https://rhtapps.redhat.com/verify?certId=140-113-325)

#### &nbsp;&nbsp;-&nbsp;Red Hat Certified System Administrator (EX200):

&nbsp;&nbsp;&nbsp;&nbsp;- `Date`: 2014-06-20

&nbsp;&nbsp;&nbsp;&nbsp;- `ID`: [140-113-325](https://rhtapps.redhat.com/verify?certId=140-113-325)

### -&nbsp;Schools:

#### &nbsp;&nbsp;-&nbsp;Gábor Dénes Főiskola:

&nbsp;&nbsp;&nbsp;&nbsp;- `Subject`: Information Technology

&nbsp;&nbsp;&nbsp;&nbsp;- `Degree`: DNF # I realized I can learn more at work than in the college

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2003-2008

&nbsp;&nbsp;&nbsp;&nbsp;- `Location`: Budapest, HU

#### &nbsp;&nbsp;-&nbsp;Móricz Zsigmond Technical School:

&nbsp;&nbsp;&nbsp;&nbsp;- `Subject`: Computersystems-Programmer

&nbsp;&nbsp;&nbsp;&nbsp;- `Institute`: Móricz Zsigmond Technical School

&nbsp;&nbsp;&nbsp;&nbsp;- `Degree`: BSc equivalent technical diploma

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2001-2003

&nbsp;&nbsp;&nbsp;&nbsp;- `Location`: Budapest, HU

#### &nbsp;&nbsp;-&nbsp;Móricz Zsigmond High School:

&nbsp;&nbsp;&nbsp;&nbsp;- `Subject`: High School specialized on Information Technology

&nbsp;&nbsp;&nbsp;&nbsp;- `Degree`: High School diploma specialized on Information Technology

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 1997-2001

&nbsp;&nbsp;&nbsp;&nbsp;- `Location`: Budapest, HU

### -&nbsp;Other:

&nbsp;&nbsp;- `Driving_license_categories`: [AM,B1,B]

## Professional_Experience:

### &nbsp;&nbsp;-&nbsp;Thermo Fisher Scientific:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2022-01-01 - nowadays

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <https://thermofisher.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: Software Engineer III

&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Maintain IaC and CI/CD in a self-hosted cloud environment, mainly using Ansible

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Anaconda`: Generate IaC setup for the firm's Anaconda service

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `backups`: implement automatic backups of our service data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `certificates`: Automate the request and update of TLS/SSL certificates among several services

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `CI/CD`: Using GitLab CI, ArgoCD, and Jenkins make sure that software changes are as smooth as possible

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Code_refactoring`: Unify and simlpify IaC

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Consul`: Implement Hashicorp Consul across our environment to be able to get metrics from ephemeral virtual machines

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `corporate_certificates`: prepare our server pool for firm-signed TLS/SSL certificates, provide tools and docs for our clients for easy migration

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `CVAT`: Deploy amnd maintain CVAT for image recognition of modern X-ray machines and microscopes

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Docker`: Set up Docker service hosting both Windows and Linux containers on Windows and Linux servers and vice versa

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `GitLab_performance`: test and optimize GitLab's performance and rate limiting

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `GitHub_runner`: Configure self-hosted GitHub runners for the projects which need it

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `GitLab_runner`: Configure GitLab runners for the projects which need it

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `IBM_RTC`: Maintain the out-of-support IBM Rational Team Concert plant

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `k8s`: Deploy and maintain Kubernetes infrastructure

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Keycloak`: Deploy and configure Keycloak in k8s to mirror corporate SSO ro our servers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Loki`: Deploy and configure Loki in k8s to analyze and alert on logs

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Monitoring_upgrade`: Switch our monitoring plant from Nagios to Prometheus

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `NIST`: Apply NIST standards to our infrastructure

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Structurizr`: deploy Structurizr on-premises for our clients with AD integration and group restriction

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Anaconda, Ansible, CentOS, CVAT, Docker, GitLab, IBM_RTC, Jenkins, K8s, Keycloak, MongoDB, OpenStack, PostgreSQL, Prometheus, Python, Tanzu, Ubuntu, vSphere, Windows_server]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Modern_medicine`: I never imagined before how much Linux servers are behind the tools doctors use nowadays

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Yak_shaving`: Distractions are sometimes very important

### &nbsp;&nbsp;-&nbsp;Toptal:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2021-11-01 - 2021-12-31

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <https://toptal.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: CI Engineer

&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Develop continuous integration scripts using Ansible

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Ansible, AWS, Azure, Github, Python, Ubuntu]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Freelance`: Freelance projects provide much higher income than full-time employment

### &nbsp;&nbsp;-&nbsp;Wandera:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2020-10-05 - 2021-09-30

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <https://wandera.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: Operations Engineer

&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Maintain IaC in a multi-provider cloud-sceptical environment

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Monitoring_upgrade`: Bring the company's monitoring stack to latest-and-greatest all across our plant

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `k3s`: Deploy and maintain lightweight Kubernetes on most of our cloud infrastructure

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Virtual_datacenter_builds`: Write and apply the code for several new virtual datacenters across the globe over several cloud providers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Proxy_upgrades`: Design and apply the upgrade of our global Squid plant

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `IPSec_tunnels`: Add dedicated IPSec tunnels to new customers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Dedicated_datacenters`: Set up dedicated virtual datacenters for bigger customers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Code_refactoring`: Unify and simlpify IaC for all old and new customers and datacenters

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Terraform_upgrade`: Upgrade our code base to be compatible with Terraform 0.13

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AWS, Azure, Bitbucket, Equinix_cloud, Github, IBM_Cloud, IPSec, Jenkins, K3s, K8s, MongoDB, OpenTelekomCloud, PostgreSQL, Prometheus, Puppet, Python, RabbitMQ, RDS, Squid, Terraform, Ubuntu, WireGuard]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Tech`: I got hands-on experience with diverse cloud providers, widened my Terraform knowledge and learnt plenty of new technology, too

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Acquisitions`: When an employer is purchased by another company, rules might change a lot

### &nbsp;&nbsp;-&nbsp;Tieto:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2019-09-02 - 2020-04-24

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <https://www.tieto.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: DevOps consultant (self-employed)

&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Develop CI/CD for Tieto's products, with a wide range of IaC toolset to meet all the requirements of management, developers, QA and production

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `BizTalk`: Develop continuous integration/continuous delivery environment, mainly focusing on automated install and configuration of BizTalk server and the backing database

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Migration_services`: Automate the install of database migration services

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Ansible, Microsoft_BizTalk, Microsoft_SQL_Server, OpenStack, Oracle, Windows_Server]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Czech_bureaucracy`: starting one's own company is not that scary as it sounds for the first time for a foreigner

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Teamwork`: not only about professional, but also interpersonal relationships

### &nbsp;&nbsp;-&nbsp;Blackboard:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2015-05-04 - 2019-08-31

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <http://blackboard.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: DevOps engineer

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Departments:

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Transact:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2018-08-27 - 2019-08-31

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Develop CI/CD for Transact product line, with a wide range of IaC toolset to meet all the requirements of management, developers, QA and production

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Attendance`: Fine-tune the QA environment

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Campus_Cash`: Develop continuous integration/continuous delivery environment

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Ansible, Azure, JenkinsX, Katalon, Kubernetes, Octopus_Deploy, PowerShell, Terraform, Windows_Server]

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;K12:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2015-05-04 - 2018-08-27

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Maintain several K-12 (primary to high school) SAAS products for global customers, including monitoring, troubleshooting, software- and hardware-related issues on a wide range of platforms

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `AWS_test_environment`: Build and maintain automated test infrastructure for the Web Community Manager product, develop self-service and reporting toolset for QA staff, set up fault tolerance and self repair

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Connect`: Maintain the product at <https://www.blackboard.com/notification-system/blackboard-connect.html>, respond on alerts

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `ConnectTXT`: Maintain the product at <https://txttools.co.uk>, respond on alerts, migrate from self-hosted infrastructure to AWS

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `DDOS_protection`: Develop a product-independent solution for protecting our infrastrtucture from DDOS attacks, automatically recognizing robot-like behavior and temporarily blocking suspicious sources. It also includes whitelist and blacklist support for certain user agents and IP ranges

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Edline_and_GradeQuick`: Maintain the product at <http://edline.net>, respond on alerts, mitigate vulnerabilities, fix hardware failures, move the hardware server plant to the virtual cloud, migrate from Ubuntu to CentOS, build customized Apache modules for the blob servers, mitigate DDOS attacks, prepare the product to be migrated to Web Community Manager, improve the performance of backend filers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Legacy_products`: Maintain SchoolFusion, SchoolWorld, SchoolCenter and TeacherWeb products, respond on alerts, mitigate vulnerabilities, fix hardware failures, move the hardware server plant to the virtual cloud, mitigate DDOS attacks, design new database clusters, prepare the products to be migrated to SchoolWires, roll out end-of-life decommissions and regulatory backups

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Operations_takeover`: During my probation period, while perparing me for daily work all my senior coworkers left the firm, so I had to reverse-engineer and discover all the environment and keep it alive while waiting for needed talent to be recruited. I proactively helped management to choose the needed skills, while responding on alerts and fixing issues in technlology I didn't yet know much about, also fixing hardware in our Chicago datacenter. Later on I transferred all the collected knowledge to my since then joined coworkers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Parentlink`: Maintain the product at <https://www.blackboard.com/school-communication-apps/blackboard-mobile-communications-app.html>, respond on alerts, migrate from self-hosted infrastructure to AWS

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Web_Community_Manager`: Maintain the product at <http://schoolwires.com>, respond on alerts, fix hardware failures, move the hardware server plant to the virtual cloud, mitigate DDOS attacks, prepare other Engage products to be migrated to Web Community Manager

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Amazon_Linux, Ansible, Apache, AWS, Bamboo, Bash, Bitbucket, BTRFS, CentOS, Chef, Cisco_ASA, CloudWatch, EC2, F5_BigIP, FreePBX, IAM, IIS, IIS, InSpec, JaCL, Jenkins, memcached, Microsoft_SQL_Server, MongoDB, MySQL, Nagios, NetApp, NewRelic, NginX, PHP, PostgreSQL, PowerShell, Python, RDS, S3, Selenium, SNS, Solaris, SonarQube, TeamCity, TCL, TestRail, Tomcat, Ubuntu, VictorOps, vSphere, WebScreen, Windows_Server, WSGI, ZFS]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Doing_good`: Working for a company doing good (such as education-related business in this case) makes the employee feel more motivated

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Internal_employment`: I do prefer to work as an internal employee as it is much easier to agree on budgets, timelines and priorities when all involved parties work towards the exactly same goal

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `EAFP`: I learnt a very important principle for work efficiency

### &nbsp;&nbsp;-&nbsp;IBM:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2012-08-01 - 2015-04-30

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <http://ibm.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: Middleware operator

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Departments:

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Overtime_tool_development:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2014-03-01 - 2015-04-30

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Develop IBM GSDC Brno's internal software to track operations people's overtime and count their reward vacation and payment

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[LDAP, MySQL, PHP]

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Dansk_Supermarked_Gruppen:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2014-03-01 - 2015-04-30

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Tasks`: Maintain the customer's e-commerce suite, develop maintenance toolset, fine-tune web servers, servlet containers and monitoring

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Domain_sharding`: Spreading requests between the Content Delivery Network for serving the website faster on <https://www.bilka.dk>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Package_maintenance`: Configure, compile and keep up-to-date the Apache package and related modules serving <https://www.bilka.dk>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `SSL_and_SPDY_enablement`: Upgrade the <http://www.bilka.dk> plant to serve SSL-only, using the SPDY protocol

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Apache, CA_Introscope_Wily, Hybris, mod_jk, mod_pagespeed, mod_spdy, mod_ssl, Red_Hat_Satellite, RHEL, RPM, Tomcat]

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;IMT_Italy:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2012-08-01 - 2014-02-28

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `IHS`: Maintain and support our clients' Apache-based IBM HTTP Server on several platforms. Problem solving and troubleshooting issues

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Snapshot_automation`: Develop multi-platform toolset for massive snapshot of services in a diverse environment. Checking all services' current state, health, configuration and version, look for error patterns and prepare reports

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `WebSphere`: Maintain and support our clients' WebSphere Application Servers on several platforms. Problem solving and troubleshooting issues

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `WebSphere_MQ`: Maintain and support our clients' WebSphere MQ systems on several platforms. Problem solving and troubleshooting issues

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Customers:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Aedificatio, Alfa_Gomma_S.p.A., Ania, Banca_Delle_Marche, Bankadati, Bit_Systems, Bolton, Cassa_Depositi, CNH, Electrolux, Fiat_Group_Automobiles_S.p.A., Fincantieri, Firema_Transporti_S.p.A., Gruppo_COIN_S.p.A., Gruppo_PAM_S.p.A., Indesit, Interbanca_S.p.A., IVECO, Mediamarket, Miriade_SRL, Montenegro_S.p.A., PUBLITALIA, Seves_S.p.A., TRENITALIA, Zambon_group_S.p.A.]

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AIX, IHS, KSH, RHEL, WebSphere, WebSphere_MQ, Windows_Server]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Challenge`: More technical challenge means more fun

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Huge_offices`: Huge offices help to fit in the local community as plenty of citizens work at the same office

### &nbsp;&nbsp;-&nbsp;Morgan Stanley:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2008-09-29 - 2012-07-23

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <http://ms.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: UNIX L3 web infrastructure operator/engineer

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `BlueCoat`: Migrate the iMimic proxy plant to the new BlueCoat plant. Set up monitoring, content filtering and HA clustering

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `ClientLink`: Maintain the thousands of servers behind <https://secure.ms.com> including High Availability, Monitoring, installs and decommissions of the server applications

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Entitlement_checking_tool`: A script which runs through thousands of LDAP and UNIX groups to check if a user or a group should or shouldn't have access to several resources

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `FB_IPO`: Prepare the web server plant for Facebook's Initial Public Offering

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `GM_IPO`: Prepare the web server plant for General Motors' Initial Public Offering

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Intrusion_forensics`: Proactively attended the forensics and recovery of Anonymous' “Operation Aurora” attack on the firm in the end of 2009

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Matrix`: Maintain the thousands of servers behind <https://matrix.ms.com> including High Availability, Monitoring, installs and decommissions of the server applications

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `NOEnergy_IPO`: Prepare the web server plant for the Norvegian energy provider's Initial Public Offering

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Optier_Corefirst`: Set up the initial OpTier Corefirst plant for the firm's Apache and Tomcat servers

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `OSQA`: Set up the initial OSQA plant for the firm's internal use

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Outage_packs`: Develop a script to collect so-called “outage packs” for Java-based server applictions. The tool is executed on server-side issues and collects stack traces, thread- and heap dumps, also several info about the HW and the OS

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Package_maintenance`: I've been the primary maintainer of the Apache, and the Midnight Commander packages in the Firm's internal RHEL fork

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `TWiki`: Development of text mining software to separate operations-, engineering- and end-user documents

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Vignette_Portal`: Upgrade the Vignette Portal plant from version 4.3 to 7.2, develop migration tools

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Web_Plant_stack_upgrade`: Script the workflow of migrating thousands of web and app servers to the latest-and-greatest version, build custom internal modules

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Weekly_change_alerts`: Develop a tool which checks open change requests and alerts affected groups to attend the weekly planning meeting and keeps them aware of the change schedule

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AFS, Apache, BlueCoat, CA_AutoSys, CA_SiteMinder, Cisco_CSS, F5_BigIP, iMimic, JaCL, Java, Juniper, Kerberos, KSH, LDAP, LightStreamer, OpTier_Corefirst, OSQA, Perl, RHEL, RPM, ServletExec, Solaris, Sybase, TCL, Tomcat, TWiki, Vignette]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Code_of_conduct`: „Always keep your sense of humor” was the most agreeable requirement I ever signed

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Follow_the_Sun`: Global teams make operations much easier and more comfortable

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Strict_rules`: Strict rules are to help employees work together without any clash of interests

### &nbsp;&nbsp;-&nbsp;EuroMACC ltd:

&nbsp;&nbsp;&nbsp;&nbsp;- `Time`: 2006-03-01 - 2008-09-26

&nbsp;&nbsp;&nbsp;&nbsp;- `URL`: <http://euromacc.com>

&nbsp;&nbsp;&nbsp;&nbsp;- `Role`: QA engineer

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `CosmOSS`: Write automated test scripts and end-user documentation for the CosmOSS Telco Classic, CosmOSS Telco Blue, and CosmOSS Telco Quad products

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `hIPer`: Develop a multiplatform deployment tool for the product, write automated test scripts and end-user documentation

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `hIPer_Util`: Make the product available for High Availability clustering, Develop a multiplatform deployment tool for the product, write automated test scripts and end-user documentation

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `WebCare`: Write automated test scripts

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Apache, ArchLinux, AS/400, BASH, Bugzilla, CA_AutoSys, CentOS, DB2, Debian, FreeBSD, Gentoo, Heartbeat, HP-UX, Java, KSH, NFS, Oracle, PHP, PostgreSQL, Rational_Robot, Rational_TestManager, SlackWare, SQABasic, Testopia, Tomcat, Ubuntu, Windows]

#### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Automation`: Automated workflow saves plenty of time for the employee

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- `Small_companies`: Small, local companies are friendly environments to work at

## Soft_skills:

- business English
- coaching
- interviewing
- knowledge share
- working in global virtual teams

## Language_skills:

- `Czech`: intermediate
- `English`: advanced
- `German`: beginner
- `Hungarian`: native
- `Italian`: beginner

## Hobbies_and_interests:

&nbsp;&nbsp;[capoeira, cycling, demoscene, geocaching, new_technology, reading, travelling]
```

## References

[Default style sheet by Jonas D.](https://github.com/Gioni06/terminal.css)
