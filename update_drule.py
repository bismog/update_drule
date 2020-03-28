#!/usr/bin/env python
from pyzabbix import ZabbixAPI
import argparse

NEW_RULE_NAME = 'discover_new_host'
ZABBIX_API_URL = 'http://localhost/zabbix'
ZABBIX_USER = 'Admin'
ZABBIX_PASS = 'zabbix'

class DRule():
    def __init__(self, url, user, passwd):
        self.zapi = ZabbixAPI(url)
        self.zapi.login(user, passwd)
        self.drule = dict()

    def get_drule(self):
        '''
        Get something like follow:
        {
            'status': '0', 
            'proxy_hostid': '0', 
            'name': 'discover_new_host', 
            'nextcheck': '1585365748', 
            'delay': '30', 
            'druleid': '3', 
            'iprange': '192.222.1.1-200'
        }
        '''
        self.drule = self.zapi.drule.get(filter={'name': NEW_RULE_NAME})[0]

    def update_iprange(self, addrs, replace=False, remove=False):
        self.get_drule()
        if not self.drule:
            return
        ipranges = self.drule.get('iprange').split(',')
        if replace:
            drange = set(addrs)
        elif remove:
            drange = set(ipranges) - set(addrs)
            if not drange:
                # Can't remove all discovery addresses, nothing to do
                print('Can not remove all discovery addresses, nothing to do')
                return
        else: 
            drange = set(ipranges) | set(addrs)

        self.drule.update({'iprange': ','.join(drange)})
        dchecks = [
            {'dcheckid': 3}
        ]
        self.drule.update(dict(dchecks=dchecks))
        self.zapi.drule.update(self.drule)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--replace', action='store_true',
        help='Replace discovery ip range to specified.')
    parser.add_argument('-R', '--remove', action='store_true',
        help='Remove discovery hosts addresses.')
    parser.add_argument('addresses', nargs='+', type=str, 
        help='Discovery ip addresses.')
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = get_args()
    dr = DRule(ZABBIX_API_URL, ZABBIX_USER, ZABBIX_PASS)
    dr.update_iprange(args['addresses'], replace=args['replace'], remove=args['remove'])

