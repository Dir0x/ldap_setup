#!/bin/bash

apt update
apt upgrade -y
apt install libpam-ldap libnss-ldap ldap-utils -y
sed -i 's/files systemd/files systemd ldap/g' /etc/nsswitch.conf 
sed -i 's/files dns/files mdns4_minimal [NOTFOUND=return] dns/g' /etc/nsswitch.conf
sed -i 's/use_authtok//g' /etc/pam.d/common-password
echo "session required pam_mkhomedir.so skel=/etc/skel umask=077" | tee -a /etc/pam.d/common-session
