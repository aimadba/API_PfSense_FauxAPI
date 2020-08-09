import base64
import os, sys, json, base64
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import uuid

# Authentification
fauxapi_host = '192.168.10.1:443'
fauxapi_apikey = "PFFAHYFVOBypX4q6scq8yILq"
fauxapi_apisecret = "8fwuQzc0BXZcnuSRwptb3xIJlrSZHoSRksxU0cEAcKooj0px0eUNlkjBeFF6"

FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=True)


# chemin vers les certificats
c_key = "/home/user/certs/server.key"
c_crt = "/home/user/certs/server.crt"
u_key = "/home/user/certs/client.key"
u_crt = "/home/user/certs/client.crt"

# les arguments 
type = sys.argv[1]
n_ca = sys.argv[2]
n_cert = sys.argv[3]


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

# recupere l'id de CA donne en argument
def recup_id_ca(x):
    ca = FauxapiLib.config_get()
    for i in ca['ca']:
        if i['descr'] == x:
            break
        else:
            continue
    return i['refid']

# verifier l'unicite du nom de la certificat
def verify_name(cert_name):
     cert = FauxapiLib.config_get()
     for i in cert['cert']:
        if i['descr'] == cert_name:
          print("--> Cert deja exist avec le meme Nom")
          exit(0)
        else:
           continue
     return cert_name



# fonction pour ajouter la certificat au fichier config.xml
def Add_cert(type,n_ca,n_cert):
    if type == "user":
        id2 = gen_id()
        cert = {
            'caref': recup_id_ca(n_ca),
            'type': '',
            'crt': file_to_var(u_crt).decode("utf-8"),
            'descr': '',
            'prv': file_to_var(u_key).decode("utf-8"),
            'refid': id2,
        }

        s = recup_config()   
        new_config = {
                'cert': s['cert']
            }
        cert['type'] = type     
        cert['descr'] = verify_name(n_cert)
        new_config['cert'].append(cert)
        res = FauxapiLib.config_patch(new_config)
        if res['message'] != 'ok':
            print(' --> Erreur lors de la creation de Cert User', res['message'])
        else:
            print(" --> Cert User creer avec Succes!!")
    elif type == "server":
        id2 = gen_id()
        cert = {
            'caref': recup_id_ca(n_ca),
            'type': '',
            'crt': file_to_var(c_crt).decode("utf-8"),
            'descr': '',
            'prv': file_to_var(c_key).decode("utf-8"),
            'refid': id2,
        }
        s = recup_config()
        new_config = {
                'cert': s['cert']
            }
        cert['type'] = type
        cert['descr'] = verify_name(n_cert) 
        new_config['cert'].append(cert)
        res = FauxapiLib.config_patch(new_config)
        if res['message'] != 'ok':
            print(' --> Erreur lors de la creation de Cert Server', res['message'])
        else:
            print(" --> Cert Server creer avec Succes!!")

Add_cert(type,n_ca,n_cert)
