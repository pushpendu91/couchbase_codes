#!/usr/bin/python2


import requests
import json
from requests.auth import HTTPBasicAuth
import ast
import re

resp = requests.get('http://ec2-18-191-83-128.us-east-2.compute.amazonaws.com:8091/indexStatus/', auth=HTTPBasicAuth('admin', 'admin1234'))

if resp.status_code != 200:
        print('GET /indexStatus/ {}'.format(resp.status_code))

json_ob=resp.json()

id_dict = {}
id_list = []
for index in json_ob["indexes"]:
        id_list.append(index["id"])
        id = index["id"]
        data = str(index["definition"])

        x = re.search('({.+})', data).group(0)
        y = re.search(r'num_replica', x)
        if y:
            z = ast.literal_eval(str(x))
            dict1 = {str(id) : z['num_replica']}
            id_dict.update(dict1)


for key,value in id_dict.items():
    id_count = id_list.count(int(key))
    if id_count == value + 1 :
        print('OK')
    else:
        print('ALERT')

