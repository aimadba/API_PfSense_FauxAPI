#!/usr/bin/python3

import os, sys, json
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import bcrypt
import random

# Authentification
fauxapi_host = '192.168.10.1:443'
fauxapi_apikey = "PFFAHYFVOBypX4q6scq8yILq"
fauxapi_apisecret = "8fwuQzc0BXZcnuSRwptb3xIJlrSZHoSRksxU0cEAcKooj0px0eUNlkjBeFF6"


# fonction qui permet de la recuperation de la config total
def recup_config():
    config = FauxapiLib.config_get()
    return config

#fonction qui permet de genere un id unique
def G_id():
  idd = random.randint(1, 4000)
  groupe = FauxapiLib.config_get('system')
  for i in groupe['group']:
     if i['gid'] == idd:
        print("--> Un groupe avec le meme Group_id deja exist")
        exit(0)
     else:
        continue
  return str(idd)

# fonction qui verifie l'existance d'un groupe avec le meme nom
def verify_name(groupname):
     group = FauxapiLib.config_get('system')
     for i in group['group']:
        if i['name'] == groupname:
          print("--> Un Groupe avec le meme Nom deja exist")
          exit(0)
        else:
           continue
     return groupname

#Fonction pour ajout d'un groupe
def Add_group(groupname):
        group = {
            'scope': 'user',
            'descr': '',
            'name': verify_name(groupname=groupname),
            'gid': G_id(),
        }
        s = recup_config()
        #cree la structure et l'ajout des info de groupe
        new_config = {
                'system': {
                   'group': s['system']['group']
                }
            }
        new_config['system']['group'].append(group)
        # envoi la nouvelle config au pfsense
        res = FauxapiLib.config_patch(new_config)
        if res['message'] != 'ok':
            print(" --> Erreur lors de lajoute", response['message'])
        else:
            print(" --> Groupe ajouter avec Succes!!")

# Recuperation d'un ou all groupe
def recup_group(nom):
    s = recup_config()
    if nom == "all":
        response_data = {}
        for group in s['system']['group']:
            response_data[group['name']] = group
            del(response_data[group['name']]['name'])
        print(json.dumps(response_data, sort_keys=True, indent=4 ))
    else:
        response_data = {}
        for group in s['system']['group']:
            response_data[group['name']] = group
            if response_data[group['name']]['name'] == nom:
                print(json.dumps(group, sort_keys=True, indent=4 ))
                exit(0)
            else:
                continue
        print("---> Le Group que vous avez entrer n'exist Pas")

# fonction de suppression d'un group a base de son nom
def suppression_group(nom):
    s = recup_config()
    new_config = {
            'system': {
                'group': s['system']['group']
            }
        }
    for i in list(range(len(s['system']['group']))):                  
        response_data= s['system']['group'][i]
        if response_data['name'] == nom:
            index = i

    del(new_config['system']['group'][index])
    res = FauxapiLib.config_patch(new_config)
    if res['message'] != 'ok':
        print(" --> Erreur lors du suppression du group", response['message'])
    else:
        print(" --> Group supprimer avec Succes!!")



# initialisation de la connexion

FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=True)

Add_group(groupname="e")
#recup_group(nom="N_group")





