#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from novaclient.client import Client
import json
import csv

def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d

nova_credentials = get_nova_credentials_v2()
nova_client = Client(**nova_credentials)
vms = nova_client.servers.list(detailed=True,search_opts={'all_tenants':'1'})
#vms = nova_client.servers.list()
#print vms

nova_info=[]
for vv in vms:
    vms_id = vv.id
    vms_name = vv.name
    vms_status = vv.status
    vms_tenant_id =vv.tenant_id
    vms_vlan = vv.addresses
    for (k,v) in vms_vlan.items():
        vms_ip = v[0]['addr']
    nova_info.append({'vm_tenant_id':vms_tenant_id,'vm_id':vms_id,'vm_status':vms_status,'vm_ip':vms_ip,'vm_name':vms_name})
print json.dumps(nova_info, sort_keys=True, indent=4)

#o = nova_info
#
#def loop_data(o, k=''):
#    global json_ob, c_line
#    if isinstance(o, dict):
#        for key, value in o.items():
#            if(k==''):
#                loop_data(value, key)
#            else:
#                loop_data(value, k + '.' + key)
#    elif isinstance(o, list):
#        for ov in o:
#            loop_data(ov, k)
#    else:
#        if not k in json_ob:
#            json_ob[k]={}
#        json_ob[k][c_line]=o
#
#def get_title_rows(json_ob):
#    title = []
#    row_num = 0
#    rows=[]
#    for key in json_ob:
#        title.append(key)
#        v = json_ob[key]
#        if len(v)>row_num:
#            row_num = len(v)
#        continue
#    for i in range(row_num):
#        row = {}
#        for k in json_ob:
#            v = json_ob[k]
#            if i in v.keys():
#                row[k]=v[i]
#            else:
#                row[k] = ''
#        rows.append(row)
#    return title, rows
#
#def write_csv(title, rows, csv_file_name):
#    with open(csv_file_name, 'w') as csv_file:
#        writer = csv.DictWriter(csv_file, fieldnames=title)
#        writer.writeheader()
#        writer.writerows(rows)
#
#def json_to_csv(object_list):
#    global json_ob, c_line
#    json_ob = {}
#    c_line = 0
#    for ov in object_list :
#        loop_data(ov)
#        c_line += 1
#    title, rows = get_title_rows(json_ob)
#    write_csv(title, rows, 'nova_get.csv')
#
#json_to_csv(o)
#

