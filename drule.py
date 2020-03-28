from pyzabbix import ZabbixAPI
ZABBIX_API_URL="http://localhost/zabbix"
zapi = ZabbixAPI(ZABBIX_API_URL)
zapi.login("Admin", "zabbix")
drule = zapi.drule.get()
print(drule)
