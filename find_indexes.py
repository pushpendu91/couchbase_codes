#!/usr/bin/python2


import requests
import json
from requests.auth import HTTPBasicAuth
import ast
import re

resp = requests.get('http://ec2-18-220-35-206.us-east-2.compute.amazonaws.com:8091/indexStatus', auth=HTTPBasicAuth('admin', 'admin1234'))

if resp.status_code != 200:
        print('GET /indexStatus/ {}'.format(resp.status_code))

json_ob=resp.json()

id_dict = {}
id_list = []
for index in json_ob["indexes"]:
    id_list.append(index["id"])
    id = index["id"]
    host = index["hosts"]
    data = str(index["definition"])

    #Check if num_replica is present in definition or not
    chk = re.search(r'num_replica', data)
    if chk:
        x = re.search('({.+})', data).group(0)
        z = ast.literal_eval(str(x))
        dict1 = {str(id) : z['num_replica']}
        id_dict.update(dict1)
    else:
        #Check for defer_build do not give alert.....
        chk1 = re.search(r'defer_build', data)
        if chk1:
            pass
        else:
            print('ALERT : NO REPLICA for id={}'.format(id))

#print(id_dict)
#print(id_list)
if len(id_dict) > 0:
    for key,value in id_dict.items():
        id_count = id_list.count(int(key))
        if id_count == value + 1 :
            print('OK')
        else:
            print('ALERT : NODE COUNT NOT MATCHING WITH REPLICA NUM for id={}..PLEASE CHECK'.format(key))

