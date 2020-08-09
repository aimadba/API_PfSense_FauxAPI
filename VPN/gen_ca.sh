#!/bin/bash

BOLD=$(tput bold)
CLEAR=$(tput sgr0)

echo -e "${BOLD}Generating RSA AES-256 Private Key for Root Certificate Authority${CLEAR}"
sudo openssl genrsa -out /home/user/certs/Root_CA.key 4096

echo -e "${BOLD}Generating Certificate for Root Certificate Authority${CLEAR}"
sudo openssl req -x509 -new -sha256 -nodes  -key /home/user/certs/Root_CA.key \
          -subj "/C=FR/ST=REIMS/O=univ/CN=pfsense" \
          -days 1825 \
          -out /home/user/certs/Root_CA.crt

echo -e "${BOLD}Generating RSA Private Key for Server Certificate${CLEAR}"
sudo openssl genrsa -out /home/user/certs/server.key 4096

echo -e "${BOLD}Generating Certificate Signing Request for Server Certificate${CLEAR}"
sudo openssl req -nodes -new -key /home/user/certs/server.key \
        -subj "/C=FR/ST=REIMS/O=univ/CN=pfsense" \
        -out /home/user/certs/server.csr

echo -e "${BOLD}Generating Certificate for Server Certificate${CLEAR}"
sudo openssl x509 -sha256 -req -in /home/user/certs/server.csr -days 3650 -CA /home/user/certs/Root_CA.crt -CAkey /home/user/certs/Root_CA.key -CAcreateserial -out /home/user/certs/server.crt -extfile /home/user/certs/v3_s.ext

echo -e "${BOLD}Generating RSA Private Key for Client Certificate${CLEAR}"
sudo openssl genrsa -out /home/user/certs/client.key 4096

echo -e "${BOLD}Generating Certificate Signing Request for Client Certificate${CLEAR}"
sudo openssl req -nodes -new -key /home/user/certs/client.key \
             -subj "/C=FR/ST=REIMS/O=univ/CN=pfsense" \
             -out /home/user/certs/client.csr

echo -e "${BOLD}Generating Certificate for Client Certificate${CLEAR}"
sudo openssl x509 -req -in /home/user/certs/client.csr -CA /home/user/certs/Root_CA.crt -CAkey /home/user/certs/Root_CA.key -CAcreateserial -out /home/user/certs/client.crt -days 1825 -sha256 -extfile /home/user/certs/v3_c.ext

echo "Done!"
