import datetime
import base64
import os, sys, json
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import random

# Authentification
fauxapi_host = '192.168.10.1:443'
fauxapi_apikey = "PFFAHYFVOBypX4q6scq8yILq"
fauxapi_apisecret = "8fwuQzc0BXZcnuSRwptb3xIJlrSZHoSRksxU0cEAcKooj0px0eUNlkjBeFF6"

FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=True)

# les arguments 
nom_ca = sys.argv[1]
nom_cert = sys.argv[2]

# chemin vers certificat TLS 
chemin = "/home/user/certs/tls.key"

# recupere le fichier config.xml
def recup_config():
    config = FauxapiLib.config_get()
    return config

# genere un ID pour la vpn
def verify_vpi_id():
    idd = random.randint(1, 100)
    vpn_servers = FauxapiLib.config_get('openvpn')
    for i in vpn_servers['openvpn-server']:
        if i['vpnid'] == idd:
            print("--> Vpn_ID deja exist")
            exit(0)
        else:
            continue
    return str(idd)

# recupere l'id de CA donne en argument
def recup_id_ca(x):
    ca = FauxapiLib.config_get()
    for i in ca['ca']:
        if i['descr'] == x:
            break
        else:
            continue
    return i['refid']

# recupere l'id de Cert donne en argument
def recup_id_cert(x):
    cert = FauxapiLib.config_get()
    for i in cert['cert']:
        if i['descr'] == x:
            break
        else:
            continue
    return i['refid']

# verifier l'unicite du port utilise par le vpn
def verify_port(p_vpn):
     vpn = FauxapiLib.config_get('openvpn')
     for i in vpn['openvpn-server']:
        if i['local_port'] == p_vpn:
          print("--> VPN  deja exist avec le meme Nom")
          exit(0)
        else:
           continue
     return p_vpn


#convertir le contenu du certificat vers un variable
def file_to_var(d):
  f = open(d,'rb')
  res = base64.b64encode(f.read())
  return res

#genere un cle TLS
def generate_tls_key(chemin):
    key = os.system("openvpn --genkey --secret "+chemin)
    if key != 0:
        print("Erreur Creation cle TLS ")
    else:
        f = open(chemin, 'rb')
        res = base64.b64encode(f.read())
        return res


# fonction pour ajouter le VPN au fichier config.xml
def Add_VPN_SRV():
    vpnserver = {
                "vpnid": verify_vpi_id(),
                "mode": "p2p_tls",
                "authmode": "Local Database",
                "protocol": "UDP4",
                "dev_mode": "tun",
                "interface": "wan",
                "local_port": verify_port("1195"),
                "description": "VPN_tls_api_final_test",
                "tls": generate_tls_key(chemin).decode("utf-8"),
                "tls_type": "auth",
                "tlsauth_keydir": "default",
                "caref": recup_id_ca(nom_ca),
                "certref": recup_id_cert(nom_cert),
                "dh_length": "2048",
                "ecdh_curve": "none",
                "cert_depth": "1",
                "crypto": "AES-128-CBC",
                "digest": "SHA256",
                "engine": "none",
                "tunnel_network": "192.168.90.0/24",
                "local_network": "172.16.10.0/24",
                "dynamic_ip": "yes",
                "topology": "subnet",
                "serverbridge_interface": "none",
                "dns_server1": "8.8.8.8",
                "exit_notify": "none",
                "netbios_ntype": "0",
                "create_gw": "both",
                "verbosity_level": "1",
                "ncp-ciphers": "AES-128-GCM",
                "ncp_enable": "enabled",
                "ping_method": "keepalive",
                "keepalive_interval": "10",
                "keepalive_timeout": "60",
                "ping_seconds": "10",
                "ping_action": "ping_restart",
                "ping_action_seconds": "60",
                "inactive_seconds": "0"
    }
    s = recup_config()
    new_config = {
        'openvpn': {
            'openvpn-server': s['openvpn']['openvpn-server']
        }
    }
    new_config['openvpn']['openvpn-server'].append(vpnserver)
    res = FauxapiLib.config_patch(new_config)
    if res['message'] != 'ok':
        print(' --> Erreur lors de la creation de VPN_SERVER', response['message'])
    else:
        print(" --> VPN_SERVER creer avec Succes!!")



Add_VPN_SRV()
