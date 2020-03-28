I found one sql script is enough for zabbix store discovery rules in database:
```
mysql zabbix -e 'update drules set iprange="xxx" where name=".."'
```

