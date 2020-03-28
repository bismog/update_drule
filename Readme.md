I found one sql script is enough for zabbix store discovery rules in database:
```
# mysql zabbix -e 'update drules set iprange="192.222.1.199,192.222.1.177" where name="discover_new_host"'
# mysql zabbix -e 'select iprange from drules where name="discover_new_host"'
+-----------------------------+
| iprange                     |
+-----------------------------+
| 192.222.1.199,192.222.1.177 |
+-----------------------------+
```

