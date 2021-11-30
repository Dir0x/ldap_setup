#!/bin/bash

# Utilización: ./install.sh daniel.local uos.ldif 192.168.1.100
# El primer parámetro es el dominio, el segundo el archivo para poblar con UOs y el tercero la IP del servidor

if [[ $# -eq 3 ]]; then
	dc=$(echo "dc="$1 | sed 's/\./,dc=/g') 
	admin=cn=admin,$dc

	apt update
	apt upgrade -y
	apt install slapd ldap-utils -y
	systemctl restart slapd
	dpkg-reconfigure slapd
	sed -i 's/REPLACE/$dc/g' $2
	ldapadd -x -D $admin -W -f $2
	apt install phpldapadmin -y

	sed -i "s/\$servers->setValue('server','name','My LDAP Server');/\$servers->setValue('server','name','$1');/g" /etc/phpldapadmin/config.php
	sed -i "s/\$servers->setValue('server','host','127.0.0.1');/\$servers->setValue('server','host','$3');/g" /etc/phpldapadmin/config.php
	sed -i "s/\$servers->setValue('server','base',array('dc=example,dc=com'));/\$servers->setValue('server','base',array('$dc'));/g" /etc/phpldapadmin/config.php
	sed -i "s/\$servers->setValue('login','bind_id','cn=admin,dc=example,dc=com');/\$servers->setValue('login','bind_id','$admin');/g" /etc/phpldapadmin/config.php
	sed -i "s/\/\/ \$config->custom->appearance['hide_template_warning'] = false;/\$config->custom->appearance['hide_template_warning'] = true;/g" /etc/phpldapadmin/config.php
	systemctl restart slapd
else
	echo "Utilización: ./install.sh daniel.local uos.ldif 192.168.1.100"
fi
