#!/usr/bin/python3
import os, sys, json
import random
import uuid
import time
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi


# Authentification
fauxapi_host = '192.168.10.1:443'
fauxapi_apikey = "PFFAHYFVOBypX4q6scq8yILq"
fauxapi_apisecret = "8fwuQzc0BXZcnuSRwptb3xIJlrSZHoSRksxU0cEAcKooj0px0eUNlkjBeFF6"


FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=True)

# fonction qui permet de la recuperation de la config total
def recup_config():
    config = FauxapiLib.config_get()
    return config

#fonction qui permet de genere un id unique a base du temps
def track():
    tr = int(round(time.time() * 1000))
    return str(tr)

def Add_RULES():
        t = track()
        rule =   {
                "id": "",
                "tracker": t,
                "type": "pass",
                "interface": "lan",
                "ipprotocol": "inet",
                "tag": "",
                "tagged": "",
                "max": "",
                "max-src-nodes": "",
                "max-src-conn": "",
                "max-src-states": "",
                "statetimeout": "",
                "statetype": "keep state",
                "os": "",
                "protocol": "tcp",
                "source": {
                    "network": "lan"
                },
                "destination": {
                    "any": "",
                },
                "descr": "Test_rule",
                "created": {
                    "time": t,
                    "username": ""
                }
        }
        s = recup_config()
        #cree la structure et l'ajout des info de l'utilisateur
        new_config = {
                'filter': {
                   'rule': s['filter']['rule']
                }
            }
        new_config['filter']['rule'].append(rule)
        # envoi la nouvelle config au pfsense
        res = FauxapiLib.config_patch(new_config)
        if res['message'] != 'ok':
            print(' --> Erreur lors de la creation du Regle', res['message'])
        else:
            print(" --> Regle creer avec Succes!!")





Add_RULES()



