# 402
Generate HTML CV (with a response code of 402 - payment required ;)) from Markdown and add client IP as a tag to my e-mail address so I now from where they really contact me without having to check my mailserver logs

## SystemD service example

```
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

[Install]
WantedBy=multi-user.target
```

## Apache config example

```
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

I formatted the below output to be YAML-parsable, because why not

# --- # 402 - Payment required - i.e. Curriculum Vitae

## Personal_Information

* `Name`: Ákos Péter BALLA
* `Date_of_Birth`: DD/MM/YYYY

### &nbsp;&nbsp;-&nbsp;Postal_address

* `CZ`: 602 00. Brno, Ulice 123/45.
* `HU`: 1046. Budapest, Utcanév utca 67.

### &nbsp;&nbsp;-&nbsp;Telephone

* `CZ`: +420.*864
* `HU`: +36.*sha.

### &nbsp;&nbsp;-&nbsp;Internet

* `Email`: <noreply@balla.cloud>
* `WWW`: <https://402.balla.cloud>
* `LinkedIn`: <https://www.linkedin.com/in/akosballa>
* `GitHub`: <https://github.com/suhancz>

## Education

### &nbsp;&nbsp;-&nbsp;Certificates

#### &nbsp;&nbsp;&nbsp;-&nbsp;Red Hat Certified Specialist in Ansible Automation (EX407)

* `Date`: 12/09/2017
* `ID`: 140-113-325

#### &nbsp;&nbsp;&nbsp;-&nbsp;Red Hat Certified Engineer (EX300)

* `Date`: 19/09/2014
* `ID`: 140-113-325

#### &nbsp;&nbsp;&nbsp;-&nbsp;Red Hat Certified System Administrator (EX200)

* `Date`: 20/06/2014
* `ID`: 140-113-325

### &nbsp;&nbsp;Schools

#### &nbsp;&nbsp;&nbsp;-&nbsp;Gábor Dénes Főiskola

* `Subject`: Information Technology
* `Degree`: DNF # I realized I can learn more at work than in the college
* `Time`: 2003-2008
* `Location`: Budapest, HU

#### &nbsp;&nbsp;&nbsp;-&nbsp;Móricz Zsigmond Technical School

* `Subject`: Computersystems-Programmer
* `Institute`: Móricz Zsigmond Technical School
* `Degree`: BSc equivalent technical diploma
* `Time`: 2001-2003
* `Location`: Budapest, HU

#### &nbsp;&nbsp;&nbsp;-&nbsp;Móricz Zsigmond High School

* `Subject`: High School specialized on Information Technology
* `Degree`: High School diploma specialized on Information Technology
* `Time`: 1997-2001
* `Location`: Budapest, HU

## Professional_Experience

### &nbsp;&nbsp;-&nbsp;Thermo Fisher Scientific

* `Time`: 01/01/2022-nowadays
* `URL`: <https://thermofisher.com>
* `Role`: Software Engineer III
* `Tasks`: Maintain IaC and CI/CD in a self-hosted cloud environment, mainly using Ansible

#### &nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `Anaconda`: Generate IaC setup for the firm's Anaconda service
* `backups`: implement automatic backups of our service data
* `certificates`: Automate the request and update of TLS/SSL certificates among several services
* `CI/CD`: Using GitLab CI, ArgoCD, and Jenkins make sure that software changes are as smooth as possible
* `Code_refactoring`: Unify and simlpify IaC
* `CVAT`: Deploy amnd maintain CVAT for image recognition of modern X-ray machines and microscopes
* `Docker`: Set up Docker service hosting both Windows and Linux containers on Windows and Linux servers and vice versa
* `GitLab_runner`: Configure GitLab runners for the projects which need it
* `IBM_RTC`: Maintain the out-of-support IBM Rational Team Concert plant
* `k8s`: Deploy and maintain Kubernetes infrastructure
* `Monitoring_upgrade`: Switch our monitoring plant from Nagios to Prometheus

#### &nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

      - [Anaconda, Ansible, CentOS, CVAT, Docker, GitLab, IBM_RTC, Jenkins, K8s, MongoDB, OpenStack, PostgreSQL, Prometheus, Python, Tanzu, Ubuntu, vSphere, Windows_server]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Goals`: Good company goals can motivate the employee a lot
* `Modern_medicine`: I never imagined before how much Linux servers are behind the tools doctors use nowadays

### &nbsp;&nbsp;-&nbsp;Wandera

* `Time`: 05/10/2020-30/09/2021
* `URL`: <https://wandera.com>
* `Role`: Operations Engineer
* `Tasks`: Maintain IaC in a multi-provider cloud-sceptical environment

#### &nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `Monitoring_upgrade`: Bring the company's monitoring stack to latest-and-greatest all across our plant
* `k3s`: Deploy and maintain lightweight Kubernetes on most of our cloud infrastructure
* `Virtual_datacenter_builds`: Write and apply the code for several new virtual datacenters across the globe over several cloud providers
* `Proxy_upgrades`: Design and apply the upgrade of our global Squid plant
* `IPSec_tunnels`: Add dedicated IPSec tunnels to new customers
* `Dedicated_datacenters`: Set up dedicated virtual datacenters for bigger customers
* `Code_refactoring`: Unify and simlpify IaC for all old and new customers and datacenters
* `Terraform_upgrade`: Upgrade our code base to be compatible with Terraform 0.13

#### &nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

      - [AWS, Azure, Bitbucket, Equinix_cloud, Github, IBM_Cloud, IPSec, Jenkins, K3s, K8s, MongoDB, OpenTelekomCloud, PostgreSQL, Prometheus, Puppet, Python, RabbitMQ, RDS, Squid, Terraform, Ubuntu, WireGuard]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Tech`: I got hands-on experience with diverse cloud providers, widened my Terraform knowledge and learnt plenty of new technology, too
* `Acquisitions`: When an employer is purchased by another company, rules might change a lot

### &nbsp;&nbsp;-&nbsp;Tieto

* `Time`: 02/09/2019-24/04/2020
* `URL`: <https://www.tieto.com>
* `Role`: DevOps consultant (self-employed)
* `Tasks`: Develop CI/CD for Tieto's products, with a wide range of IaC toolset to meet all the requirements of management, developers, QA and production

#### &nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `BizTalk`: Develop continuous integration/continuous delivery environment, mainly focusing on automated install and configuration of BizTalk server and the backing database
* `Migration_services`: Automate the install of database migration services

#### &nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

      - [Ansible, Microsoft_BizTalk, Microsoft_SQL_Server, OpenStack, Oracle, Windows_Server]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Czech_bureaucracy`: starting one's own company is not that scary as it sounds for the first time for a foreigner
* `Teamwork`: not only about professional, but also interpersonal relationships

### &nbsp;&nbsp;-&nbsp;Blackboard

* `Time`: 04/05/2015-31/08/2019
* `URL`: <http://blackboard.com>
* `Role`: DevOps engineer

#### &nbsp;&nbsp;&nbsp;-&nbsp;Departments

##### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Transact

* `Time`: 27/08/2018-31/08/2019
* `Tasks`: Develop CI/CD for Transact product line, with a wide range of IaC toolset to meet all the requirements of management, developers, QA and production

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `Attendance`: Fine-tune the QA environment
* `Campus_Cash`: Develop continuous integration/continuous delivery environment

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

            - [Ansible, Azure, JenkinsX, Katalon, Kubernetes, Octopus_Deploy, PowerShell, Terraform, Windows_Server]

##### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;K12

* `Time`: 04/05/2015-27/08/2018
* `Tasks`: Maintain several K-12 (primary to high school) SAAS products for global customers, including monitoring, troubleshooting, software- and hardware-related issues on a wide range of platforms

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `AWS_test_environment`: Build and maintain automated test infrastructure for the Web Community Manager product, develop self-service and reporting toolset for QA staff, set up fault tolerance and self repair
* `Connect`: Maintain the product at <https://www.blackboard.com/notification-system/blackboard-connect.html>, respond on alerts
* `ConnectTXT`: Maintain the product at <https://txttools.co.uk>, respond on alerts, migrate from self-hosted infrastructure to AWS
* `DDOS_protection`: Develop a product-independent solution for protecting our infrastrtucture from DDOS attacks, automatically recognizing robot-like behavior and temporarily blocking suspicious sources. It also includes whitelist and blacklist support for certain user agents and IP ranges
* `Edline_and_GradeQuick`: Maintain the product at <http://edline.net>, respond on alerts, mitigate vulnerabilities, fix hardware failures, move the hardware server plant to the virtual cloud, migrate from Ubuntu to CentOS, build customized Apache modules for the blob servers, mitigate DDOS attacks, prepare the product to be migrated to Web Community Manager, improve the performance of backend filers
* `Legacy_products`: Maintain SchoolFusion, SchoolWorld, SchoolCenter and TeacherWeb products, respond on alerts, mitigate vulnerabilities, fix hardware failures, move the hardware server plant to the virtual cloud, mitigate DDOS attacks, design new database clusters, prepare the products to be migrated to SchoolWires, roll out end-of-life decommissions and regulatory backups
* `Operations_takeover`: During my probation period, while perparing me for daily work all my senior coworkers left the firm, so I had to reverse-engineer and discover all the environment and keep it alive while waiting for needed talent to be recruited. I proactively helped management to choose the needed skills, while responding on alerts and fixing issues in technlology I didn't yet know much about, also fixing hardware in our Chicago datacenter. Later on I transferred all the collected knowledge to my since then joined coworkers
* `Parentlink`: Maintain the product at <https://www.blackboard.com/school-communication-apps/blackboard-mobile-communications-app.html>, respond on alerts, migrate from self-hosted infrastructure to AWS
* `Web_Community_Manager`: Maintain the product at <http://schoolwires.com>, respond on alerts, fix hardware failures, move the hardware server plant to the virtual cloud, mitigate DDOS attacks, prepare other Engage products to be migrated to Web Community Manager

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

            - [Amazon_Linux, Ansible, Apache, AWS, Bamboo, Bash, Bitbucket, BTRFS, CentOS, Chef, Cisco_ASA, CloudWatch, EC2, F5_BigIP, FreePBX, IAM, IIS, IIS, InSpec, JaCL, Jenkins, memcached, Microsoft_SQL_Server, MongoDB, MySQL, Nagios, NetApp, NewRelic, NginX, PHP, PostgreSQL, PowerShell, Python, RDS, S3, Selenium, SNS, Solaris, SonarQube, TeamCity, TCL, TestRail, Tomcat, Ubuntu, VictorOps, vSphere, WebScreen, Windows_Server, WSGI, ZFS]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Doing_good`: Working for a company doing good (such as education-related business in this case) makes the employee feel more motivated
* `Internal_employment`: I do prefer to work as an internal employee as it is much easier to agree on budgets, timelines and priorities when all involved parties work towards the exactly same goal

### &nbsp;&nbsp;-&nbsp;IBM

* `Time`: 01/08/2012-30/04/2015
* `URL`: <http://ibm.com>
* `Role`: Middleware operator

#### &nbsp;&nbsp;&nbsp;-&nbsp;Departments

##### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Overtime_tool_development

* `Time`: 01/03/2014-30/04/2015
* `Tasks`: Develop IBM GSDC Brno's internal software to track operations people's overtime and count their reward vacation and payment

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

            - [LDAP, MySQL, PHP]

##### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Dansk_Supermarked_Gruppen

* `Time`: 01/03/2014-30/04/2015
* `Tasks`: Maintain the customer's e-commerce suite, develop maintenance toolset, fine-tune web servers, servlet containers and monitoring

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `Domain_sharding`: Spreading requests between the Content Delivery Network for serving the website faster on <https://www.bilka.dk>
* `Package_maintenance`: Configure, compile and keep up-to-date the Apache package and related modules serving <https://www.bilka.dk>
* `SSL_and_SPDY_enablement`: Upgrade the <http://www.bilka.dk> plant to serve SSL-only, using the SPDY protocol

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

            - [Apache, CA_Introscope_Wily, Hybris, mod_jk, mod_pagespeed, mod_spdy, mod_ssl, Red_Hat_Satellite, RHEL, RPM, Tomcat]

##### &nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;IMT_Italy

* `Time`: 01/08/2012-28/02/2014

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `IHS`: Maintain and support our clients' Apache-based IBM HTTP Server on several platforms. Problem solving and troubleshooting issues
* `Snapshot_automation`: Develop multi-platform toolset for massive snapshot of services in a diverse environment. Checking all services' current state, health, configuration and version, look for error patterns and prepare reports
* `WebSphere`: Maintain and support our clients' WebSphere Application Servers on several platforms. Problem solving and troubleshooting issues
* `WebSphere_MQ`: Maintain and support our clients' WebSphere MQ systems on several platforms. Problem solving and troubleshooting issues

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Customers

            - [Aedificatio, Alfa_Gomma_S.p.A., Ania, Banca_Delle_Marche, Bankadati, Bit_Systems, Bolton, Cassa_Depositi, CNH, Electrolux, Fiat_Group_Automobiles_S.p.A., Fincantieri, Firema_Transporti_S.p.A., Gruppo_COIN_S.p.A., Gruppo_PAM_S.p.A., Indesit, Interbanca_S.p.A., IVECO, Mediamarket, Miriade_SRL, Montenegro_S.p.A., PUBLITALIA, Seves_S.p.A., TRENITALIA, Zambon_group_S.p.A.]

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

            - [AIX, IHS, KSH, RHEL, WebSphere, WebSphere_MQ, Windows_Server]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Challenge`: More technical challenge means more fun
* `Huge_offices`: Huge offices help to fit in the local community as plenty of citizens work at the same office

### &nbsp;&nbsp;-&nbsp;Morgan Stanley

* `Time`: 29/09/2008-23/07/2012
* `URL`: <http://ms.com>
* `Role`: UNIX L3 web infrastructure operator/engineer

#### &nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `BlueCoat`: Migrate the iMimic proxy plant to the new BlueCoat plant. Set up monitoring, content filtering and HA clustering
* `ClientLink`: Maintain the thousands of servers behind <https://secure.ms.com> including High Availability, Monitoring, installs and decommissions of the server applications
* `Entitlement_checking_tool`: A script which runs through thousands of LDAP and UNIX groups to check if a user or a group should or shouldn't have access to several resources
* `FB_IPO`: Prepare the web server plant for Facebook's Initial Public Offering
* `GM_IPO`: Prepare the web server plant for General Motors' Initial Public Offering
* `Intrusion_forensics`: Proactively attended the forensics and recovery of Anonymous' “Operation Aurora” attack on the firm in the end of 2009
* `Matrix`: Maintain the thousands of servers behind <https://matrix.ms.com> including High Availability, Monitoring, installs and decommissions of the server applications
* `NOEnergy_IPO`: Prepare the web server plant for the Norvegian energy provider's Initial Public Offering
* `Optier_Corefirst`: Set up the initial OpTier Corefirst plant for the firm's Apache and Tomcat servers
* `OSQA`: Set up the initial OSQA plant for the firm's internal use
* `Outage_packs`: Develop a script to collect so-called “outage packs” for Java-based server applictions. The tool is executed on server-side issues and collects stack traces, thread- and heap dumps, also several info about the HW and the OS
* `Package_maintenance`: I've been the primary maintainer of the Apache, and the Midnight Commander packages in the Firm's internal RHEL fork
* `TWiki`: Development of text mining software to separate operations-, engineering- and end-user documents
* `Vignette_Portal`: Upgrade the Vignette Portal plant from version 4.3 to 7.2, develop migration tools
* `Web_Plant_stack_upgrade`: Script the workflow of migrating thousands of web and app servers to the latest-and-greatest version, build custom internal modules
* `Weekly_change_alerts`: Develop a tool which checks open change requests and alerts affected groups to attend the weekly planning meeting and keeps them aware of the change schedule

#### &nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

      - [AFS, Apache, BlueCoat, CA_AutoSys, CA_SiteMinder, Cisco_CSS, F5_BigIP, iMimic, JaCL, Java, Juniper, Kerberos, KSH, LDAP, LightStreamer, OpTier_Corefirst, OSQA, Perl, RHEL, RPM, ServletExec, Solaris, Sybase, TCL, Tomcat, TWiki, Vignette]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Code_of_conduct`: „Always keep your sense of humor” was the most agreeable requirement I ever signed
* `Follow_the_Sun`: Global teams make operations much easier and more comfortable
* `Strict_rules`: Strict rules are to help employees work together without any clash of interests

### &nbsp;&nbsp;-&nbsp;EuroMACC ltd

* `Time`: 01/03/2006-26/09/2008
* `URL`: <http://euromacc.com>
* `Role`: QA engineer

#### &nbsp;&nbsp;&nbsp;-&nbsp;Projects

* `CosmOSS`: Write automated test scripts and end-user documentation for the CosmOSS Telco Classic, CosmOSS Telco Blue, and CosmOSS Telco Quad products
* `hIPer`: Develop a multiplatform deployment tool for the product, write automated test scripts and end-user documentation
* `hIPer_Util`: Make the product available for High Availability clustering, Develop a multiplatform deployment tool for the product, write automated test scripts and end-user documentation
* `WebCare`: Write automated test scripts

#### &nbsp;&nbsp;&nbsp;-&nbsp;Technologies_used

      - [Apache, ArchLinux, AS/400, BASH, Bugzilla, CA_AutoSys, CentOS, DB2, Debian, FreeBSD, Gentoo, Heartbeat, HP-UX, Java, KSH, NFS, Oracle, PHP, PostgreSQL, Rational_Robot, Rational_TestManager, SlackWare, SQABasic, Testopia, Tomcat, Ubuntu, Windows]

#### &nbsp;&nbsp;&nbsp;-&nbsp;What_I_learnt

* `Automation`: Automated workflow saves plenty of time for the employee
* `Small_companies`: Small, local companies are friendly environments to work at

## Soft_skills

* business English
* coaching
* interviewing
* knowledge share
* working in global virtual teams

## Language_skills

* `Czech`: intermediate
* `English`: advanced
* `German`: beginner
* `Hungarian`: native
* `Italian`: beginner

## Hobbies_and_interests

* [capoeira, cycling, demoscene, geocaching, new_technology, reading, travelling]
