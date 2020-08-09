#!/bin/bash

#-------Vars--------------
nom_ca="bash_ca_test"
nom_cert_s="Server Certificat"
nom_cert_u="User Certificat"
n_user="vpnUser"
type="server"
type1="user"
type_u="vpn_user"
chemin="/home/user/certs/"

echo "###############################################"
echo "######|Generation des cles/certificats|########"
echo "###############################################"
echo ""
var=$(ls -a $chemin | sed -e "/\.$/d" | wc -l)

if [ $var -eq 2 ]
then
      sudo ./gent.sh
else
      echo "--> Certificats deja exists ! "
fi
echo ""
echo "###############################################"
echo "#############|Creation du CA|##################"
echo "###############################################"
echo ""
sudo python3 ca.py $nom_ca
if [ $? -ne 0 ] 
then
	echo "--> la creation du CA a echoue ! "
	exit 1
fi
echo ""
echo "###############################################"
echo "#########|Creation Cert pour VPN_SRV|##########"
echo "###############################################"
echo ""
sudo python3 cert.py $type $nom_ca $nom_cert_s
if [ $? -ne 0 ]
then
        echo "--> la creation du Cert-Server a echoue ! "
        exit 1
fi
echo ""
echo "###############################################"
echo "###########|Creation du Serveur VPN|###########"
echo "###############################################"
echo ""
sudo python3 vpn_srv.py $nom_ca $nom_cert_s
if [ $? -ne 0 ]
then
        echo "--> la creation du VPN a echoue ! "
        exit 1
fi
echo ""
echo "###############################################"
echo "######|Creation certificat pour le Client|#####"
echo "###############################################"
echo ""
sudo python3 cert.py $type1 $nom_ca $nom_cert_u
if [ $? -ne 0 ]
then
        echo "--> la creation du Cert-User a echoue ! "
        exit 1
fi
echo ""
echo "###############################################"
echo "###########|Creation User VPN|#################"
echo "###############################################"
echo ""
sudo python3 user.py $n_user $type_u $nom_cert_u
if [ $? -ne 0 ]
then
        echo "--> la creation du User a echoue ! "
        exit 1
fi
echo ""
echo "###############################################"
echo "####################|FIN|######################"



