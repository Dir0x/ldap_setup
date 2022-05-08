#!/bin/bash

# Utilización: ./install.sh daniel.local uos.ldif
# El primer parámetro es el dominio y el segundo el archivo para poblar con UOs

if [[ $# -eq 2 ]]; then
	dc=$(echo "dc="$1 | sed 's/\./,dc=/g') 
	admin=cn=admin,$dc

	apt update
	apt upgrade -y
	apt install slapd ldap-utils -y
	systemctl restart slapd
	dpkg-reconfigure slapd
	sed -i 's/REPLACE/$dc/g' $2
	ldapadd -x -D $admin -W -f $2
	systemctl restart slapd
else
	echo "Utilización: ./install.sh daniel.local uos.ldif"
fi
