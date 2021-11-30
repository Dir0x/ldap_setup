#!/usr/bin/python3

import ldap, signal, sys, string, os
import ldap.modlist as modlist
from getpass import getpass
from passlib.hash import ldap_md5_crypt

os.system("clear")
address = input("Introduce la dirección del servidor LDAP: ")
l = ldap.initialize("ldap://" + address)
l.protocol_version = ldap.VERSION3
l.set_option(ldap.OPT_REFERRALS, 0)
domain = input("Introduce el dominio: ")
base = "dc=" + domain.replace(".", ",dc=")
admin = input("Introduce el nombre de administrador: ")
password = getpass("Introduce la contraseña de administrador: ")
bind = l.simple_bind_s("cn=" + admin + "," + base, password)

def signal_handler(signal, frame):
    global run
    run = False
    print('\n\nDeteniéndose')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
	os.system("clear")
	print("1. Listar usuarios")
	print("2. Añadir usuario")
	print("3. Borrar usuario")
	print("4. Salir")

	cmd = input("Selecciona tu acción: ")

	if cmd == "1":
		os.system("clear")
		attributes = "displayName"
		criteria = "objectClass=posixAccount"
		result = l.search_s(base, ldap.SCOPE_SUBTREE, "objectClass=posixAccount", ['displayName'])
		os.system("clear")
		print("Los usuarios son:\n")
		for r in result:
			print(r[0])
		input()

	if cmd == "2":
		os.system("clear")
		ou = input("Introduzca la unidad organizativa si la hay: ")

		if ou == "":
			base_dn = base
		else:
			base_dn = "ou=" + ou + "," + base

		fullname = input("Introduzca el nombre de usuario que desea crear: ")
		dn = str('cn=' + fullname + ',' + base_dn)
		home_dir = "/home/users/" + fullname
		gid = input("Introduzca el gid: ")
		loginShell = input("Introduzca la shell del usuario: ['/bin/bash']")
		user_pass1 = 0
		user_pass2 = 1

		while user_pass1 != user_pass2:
			user_pass1 = getpass("Introduzca la contraseña para el nuevo usuario (las contraseñas deben de coincidir): ")
			user_pass2 = getpass("Confirme la contraseña: ")
		hash = ldap_md5_crypt.hash(user_pass1)

		if loginShell == "":
			loginShell = "/bin/bash"

		uidNumber = bytes(input("Introduzca el uid del usuario: "), 'UTF-8')
		entry = []
		entry.extend([
			('objectClass', [b"inetOrgPerson", b"organizationalPerson", b"posixAccount", b"person"]),
			('uid', bytes(fullname, 'UTF-8')),
			('sn', bytes(fullname, 'UTF-8')),
			('uidNumber', b"2000"),
			('gidNumber', bytes(gid, 'UTF-8')),
			('loginShell', b"/bin/bash"),
			('homeDirectory', bytes(home_dir, 'UTF-8')),
			('userPassword', bytes(hash, 'UTF-8'))
		])

		l.add_s(dn, entry)

	if cmd == "3":
		os.system("clear")
		dn = input("Introduce el dn del usuario a borrar: ")
		check = input("Seguro que desea borrar este usuario: " + dn + " [s/N]")
		check = check.upper()
		if check == "":
			check = "N"
		if check == "S":
			l.delete(dn)
		else:
			print("No se ha borrado el usuario")

	if cmd.upper() == "4":
		exit()
