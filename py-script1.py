from netmiko import ConnectHandler
from getpass import getpass
import subprocess
import os.path
import sys
import argparse

cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.50.100",
    "username": "admin",
    "password": " ",
    "secret": " "
}

def prefix_update(prefix_input, asn_input):
	prefix_list_name = str(prefix_input)
	asn = str(asn_input)
	bgpq3_command = " bgpq3 as" + asn +" -l " + prefix_list_name + " -4 -A"
	command = subprocess.check_output(bgpq3_command, encoding="utf-8", shell=True)
	list_prefix  = []

	for x in command.splitlines():
        	list_prefix.append(x)

	if os.path.isfile("prefix_list_file.txt"):
        	with open("prefix_list_file.txt") as f:
                	for x in f.readlines():
                                num_24 = 24
                                if (int(x[-3:]) <  num_24):
                                	x_prefix = "ip prefix-list " + prefix_list_name + "  permit " + x.strip("\n") + " le 24"
                                	list_prefix.append(x_prefix)
                                elif (int(x[-3:]) ==  num_24):
                                	x_prefix = "ip prefix-list " + prefix_list_name + "  permit " + x.strip("\n")
                                	list_prefix.append(x_prefix)
                                else:
                                	print ("\n")
        	print (list_prefix)
	else:
        	print("no file")

	with ConnectHandler(**cisco1) as net_connect:
        	net_connect.enable()
        	output = net_connect.send_config_set(list_prefix)
	print (output)
	net_connect.disconnect()

def main_menu():
	output_file = """1- update prefix list\n2- BGP Summary"""
	
	return output_file

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description ="Python Script")
	parser.add_argument("p", help="Prefix list name")
	parser.add_argument("a", help="AS Number")
	args = parser.parse_args()
	prefix_update(args.p, args.a)
