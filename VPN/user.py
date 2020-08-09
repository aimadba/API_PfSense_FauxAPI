#!/usr/bin/python3

import os, sys, json
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import bcrypt
import random

# Authentification
fauxapi_host = '192.168.10.1:443'
fauxapi_apikey = "PFFAHYFVOBypX4q6scq8yILq"
fauxapi_apisecret = "8fwuQzc0BXZcnuSRwptb3xIJlrSZHoSRksxU0cEAcKooj0px0eUNlkjBeFF6"

# les arguments 
nom = sys.argv[1]
type = sys.argv[2]
cert_nom = sys.argv[3]

# fonction qui permet de la recuperation de la config total
def recup_config():
    config = FauxapiLib.config_get()
    return config
# fonction qui hach le mot de passe 
def hash_password(password):
    psd = password.encode("utf-8")
    hashed = bcrypt.hashpw(psd, bcrypt.gensalt())
    return hashed

#fonction qui permet de genere un id unique
def U_id():
  idd = random.randint(1, 4000)
  users = FauxapiLib.config_get('system')
  for i in users['user']:
     if i['uid'] == idd:
        print("--> User_id deja exist")
        exit(0)
     else:
        continue
  return str(idd)

# fonction qui verifie l'existance d'un utilisateur avec le meme nom
def verify_name(username):
     users = FauxapiLib.config_get('system')
     for i in users['user']:
        if i['name'] == username:
          print("--> User_name deja exist")
          exit(0)
        else:
           continue
     return username

# recupere l'id de Certificat donne en argument
def recup_id_cert(x):
    cert = FauxapiLib.config_get()
    for i in cert['cert']:
        if i['descr'] == x:
            break
        else:
            continue
    return i['refid']


#Fonction pour ajout d'un utilisateur
def Add_user(username,type,cert):
        user = {
            'scope': 'user',
            'bcrypt-hash': hash_password("toto").decode("utf-8"),
            "priv": [
                       "page-all"
                    ],
            'descr': '',
            'name': verify_name(username),
            'expires': '',
            'dashboardcolumns': '2',
            'authorizedkeys': '',
            'ipsecpsk': '',
            'webguicss': 'pfSense.css',
            "cert": [
                    recup_id_cert(cert),
                ],
            'uid': U_id(),
        }
        s = recup_config()
        #cree la structure et l'ajout des info de l'utilisateur
        new_config = {
                'system': {
                   'user': s['system']['user']
                }
            }
        if type == "vpn_user":
                new_config['system']['user'].append(user)
                res = FauxapiLib.config_patch(new_config)
                if res['message'] != 'ok':
                    print(' --> Erreur lors de creation du VPN User', response['message'])
                else:
                    print(" --> User_VPN  ajouter avec Succes!!")
        elif type == "user":
                del(user["cert"])
                new_config['system']['user'].append(user)
                res = FauxapiLib.config_patch(new_config)
                if res['message'] != 'ok':
                    print(" --> Erreur lors du creation de l'utilisateur", response['message'])
                else:
                    print(" --> User ajouter avec Succes!!")


FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=True)

Add_user(username=nom, type=type, cert=cert_nom)


