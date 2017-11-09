#!/usr/bin/python
import re
import sys
import requests


def split_interfaces(config):
    lines = config.split('\n')
    begin = re.compile(r'auto')
    interfaces = []
    interface = []
    for line in lines:
        if line:
            if line[0] == '#':
                continue
            else:
                line = line.strip()
                match = begin.match(line)
                if match:
                    if interface:
                        interfaces.append(interface)
                    interface = [line]
                    print interface
                    print '++++++++++'
                else:
                    interface.append(line)
    interfaces.append(interface)
    return interfaces


def parse(config):
    interfaces = split_interfaces(config)
    interface_dict = {}

    def parse_interface(interface):
        iface = interface[0].split(' ')[1]
        iface_dict = {}

        for line in interface[1:]:
            parts = line.split(' ')
            if parts[0] == 'iface':
                iface_dict['bootproto'] = parts[3]
            else:
                iface_dict[parts[0]] = parts[1:]
        interface_dict[iface] = iface_dict

    for interface in interfaces:
        parse_interface(interface)
    return interface_dict


def write_config(interface_dict):
    for name, iface_dict in interface_dict.iteritems():
        if name == 'lo':
            continue
        else:
            with open('/etc/sysconfig/network-scripts/ifcfg-%s' % name, 'w') as f:
                f.write('DEVICE=%s\n' % name)

                bootproto = iface_dict.get('bootproto')
                if bootproto:
                    f.write('BOOTPROTO=%s\n' % bootproto)

                address = iface_dict.get('address')[0]
                if address:
                    f.write('IPADDR=%s\n' % address)

                netmask = iface_dict.get('netmask')[0]
                if netmask:
                    f.write('NETMASK=%s\n' % netmask)

                gateway = iface_dict.get('gateway')[0]
                if gateway and name == 'eth0':
                    f.write('GATEWAY=%s\n' % gateway)

                dns = iface_dict.get('dns-nameservers')
                if dns:
                    f.write('PEERDNS=yes\n')
                    for i, server in enumerate(dns):
                        f.write('DNS%d=%s\n' % (i + 1, server))


try:
    r = requests.get("http://169.254.169.254/openstack/latest/meta_data.json")
    json_response = r.json()
    path = json_response['network_config']['content_path']
    config = requests.get("http://169.254.169.254/openstack" + path).text
    interface_dict = parse(config)
    write_config(interface_dict)
except requests.exceptions.RequestException as e:
    print e
    sys.exit(1)
