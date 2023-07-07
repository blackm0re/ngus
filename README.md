# ngus

*ngus* is a minimalist HTTP server written in pure Python and intended for
receiving file uploads


## Motivation

The reason for writing this small package was the need to transfer files from
a Windows desktop machine running on a highly restricted VPN to my GNU and UNIX
systems.

Since the HTTP traffic (out) was not restricted, I started looking for a small
, yet flexible HTTP server that could satisfy the following criteria:

- can be configured with the help of a few CLI parameters

- can be started and stopped quickly by an unprivileged user

- be able to receive uploads to a specific directory

- be portable and require a minimal amount of dependencies

- be part of the C/C++ or Python ecosystems

To my amazement I wasn't able to find any free software matching that criteria.


## Overview

The main purpose of *ngus* is to accept file uploads as POST requests from an
HTTP client.

Currently *ngus* provides only simple encryption (HTTPS) support. Many
different tools can be employed to serve as an HTTPS proxy.

See the examples bellow for more details!


## Installation

### pip (pypi)

   ```bash
   pip install ngus
   ```


### Gentoo

   ```bash
   # add sgs' custom repository using app-eselect/eselect-repository
   eselect repository add sgs

   emerge www-servers/ngus
   ```


## Examples

When installing *ngus* as described above, a dedicated *ngus* script
(entry point) will be installed in addition to the *ngus* Python module.

Running:

   ```bash
   ngus -h
   ```

will be for all practical purposes the same as running:

   ```bash
   python -m ngus -h
   ```

The latter format will be used for the rest of this section.


   ```bash
   python -m ngus -H 0.0.0.0 -p 8080
   ```

will start the server, binding port 8080 on all available interfaces and
storing the received uploads in the current working directory (CWD), while

   ```bash
   python -m ngus -H 0.0.0.0 -p 8080 -u /home/s/uploads
   ```

will store them in `/home/s/uploads`

**Note:** This will allow *ngus* to replace any existing file in this directory.

Once the server is running a client will be able to send a POST form with a
file data. One can always access the URL (send a GET request) with a regular
browser and use the provided form or simply use a client like *curl* for
posting (sending a POST request) a form.

   ```bash
   curl -F "ufile=@myfile.zip" http://158.39.125.240:8080
   ```

The default form input field name is *ufile*. That can be changed by using the
*--input-name* parameter. Basic auth support can be added with the
*--basic-auth* parameter.

   ```bash
   python -m ngus -H 0.0.0.0 -p 8080 -i uploadfile -b "uname:foo" -u /home/s/uploads
   curl --basic -u uname -F "uploadfile=@myfile.zip" http://158.39.125.240:8080
   ```

Simple encryption (HTTPS) support

   ```bash
   # creating a self-signed key / certificate pair valid for 356 days
   openssl req -sha256 -newkey rsa:4096 -nodes -x509 -extensions v3_ca -subj "/C=NO/O=MyOrg/CN=uploads.myhostname.net" -days 365 -keyout uploads.myhostname.net.key.pem -out uploads.myhostname.net.cert.pem
   python -m ngus -H 0.0.0.0 -p 8080 -b "uname:foo" -k uploads.myhostname.net.key.pem -c uploads.myhostname.net.cert.pem -u /home/s/uploads
   # since the certificate is self-signed, it can serve as a CA to itself in this example
   curl --basic -u uname -F "ufile=@myfile.zip" --cacert uploads.myhostname.net.cert.pem https://uploads.myhostname.net:8080
   ```


### Using *nginx* as a proxy

*ngus* will usually not be run on ports 80 (HTTP) and 443 (HTTPS) since binding
them requires administrator (root) privileges.

Running *ngus* on a unprivileged port (> 1024) may not solve the problem
described above. Namely a potential client may not be able to communicate to
ports other than 80 and 443 because of imposed firewall / VPN restrictions.

Another potential challenge arises when *ngus* runs on a host that is not
publicly accessible.

*nginx* can be used to proxy the traffic toward *ngus* instance running as
described in the examples above.

   ```nginx
   server {

      listen 443 ssl;
      listen 80;
      server_name uploads.myhostname.net;

      access_log /var/log/nginx/uploads.myhostname.net.access.log;
      error_log /var/log/nginx/uploads.myhostname.net.error.log error;

      ssl_certificate uploads.myhostname.net.cert.pem;
      ssl_certificate_key uploads.myhostname.net.key.pem;

      location / {
          # point at the ngus instance running on a private network address
          proxy_pass http://158.39.125.240:8080/;
      }

   }
   ```

... and then upload a file with:

   ```bash
   curl -F "ufile=@myfile.zip" https://uploads.myhostname.net
   ```


## Support and contributing

ngus is hosted on GitHub: https://github.com/blackm0re/ngus


## Author

Simeon Simeonov - sgs @ LiberaChat


## [License](https://github.com/blackm0re/ngus/blob/master/LICENSE)

Copyright (c) 2021-2023 Simeon Simeonov
All rights reserved.

[Licensed](https://github.com/blackm0re/ngus/blob/master/LICENSE) under the
GNU General Public License v3.0 or later.
SPDX-License-Identifier: GPL-3.0-or-later
