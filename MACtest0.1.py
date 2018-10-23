#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface")
    elif not options.mac:
        parser.error("[-] Please specify an mac")
    return options

def change_mac(interface, mac):
    print("[+] Changing MAC address for " + interface)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not get mac addres")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("current Mac = " + str(current_mac))
change_mac(options.interface, options.mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac:
    print("[+] MAC address was succesfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
