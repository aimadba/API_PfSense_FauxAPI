import base64
import os, sys, json, base64
from OpenSSL import crypto, SSL
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import uuid

# Authentification
fauxapi_host = '192.168.10.1:443'
fauxapi_apikey = "PFFAHYFVOBypX4q6scq8yILq"
fauxapi_apisecret = "8fwuQzc0BXZcnuSRwptb3xIJlrSZHoSRksxU0cEAcKooj0px0eUNlkjBeFF6"

FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=True)

# chemin vers les certificats
r_key = "/home/user/certs/Root_CA.key"
r_cert = "/home/user/certs/Root_CA.crt"
nom_ca = sys.argv[1]

# recupere le fichier config.xml
def recup_config():
    config = FauxapiLib.config_get()
    return config

# genere un ID pour la certificat
def gen_id():
   id = str(uuid.uuid1()).replace("-", "")[:13]
   return id

#convertir le contenu du certificat vers un variable
def file_to_var(d):
  f = open(d,'rb')
  res = base64.b64encode(f.read())
  return res

# verifier l'unicite du nom de la certificat
def verify_name(ca_name):
     ca = FauxapiLib.config_get()
     for i in ca['ca']:
        if i['descr'] == ca_name:
          print("--> CA deja exist avec le meme Nom")
          exit(0)
        else:
           continue
     return ca_name


# fonction pour ajouter la certificat au fichier config.xml
def Add_CA(nom_ca):
        id2 = gen_id()
        CA = {
            'crt': file_to_var(r_cert).decode("utf-8"),
            'descr': verify_name(nom_ca),
            'prv': file_to_var(r_key).decode("utf-8"),
            'refid': id2,
            'serial': '0',
        }

        s = recup_config()
        #cree la structure et l'ajout des info de l'utilisateur
        new_config = {
                'ca': s['ca']
            }
        new_config['ca'].append(CA)
        # envoi la nouvelle config au pfsense
        res = FauxapiLib.config_patch(new_config)
        if res['message'] != 'ok':
            print(' --> Erreur lors de la creation de CA', res['message'])
        else:
            print(" --> CA creer avec Succes!!")


Add_CA(nom_ca)
