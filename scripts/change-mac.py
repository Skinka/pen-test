# run $ sudo python3 change-mac.py -i eth0 -m random  
# change mac address
import random
import re
import subprocess  # do console command
import argparse  # parse console arguments


def get_interfaces():
    eths = []
    for line in open('/proc/net/dev', 'r'):
        if line.find(':') != -1:
            data = line.split(':')
            eths.append(data[0].strip())
    return eths


def get_random_mac():
    data = [format(random.randint(0x00, 0xff), '02x').upper() for _ in range(1, 6)]
    data.insert(0, format(random.randrange(0x00, 0xff, 2), '02x').upper())
    return ":".join(data)


def validate_interface(i):
    eths = get_interfaces()
    return i in eths


def validate_mac(m):
    if re.match("((?:[A-F0-9]{2}[:]){5}[A-F0-9]{2})$", m.upper()):
        return True
    return False


def check_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interfaceArg", help="set ether interface, ets: eth0")
    parser.add_argument("-m", "--mac", dest="macArg", help="set mac address, like XX:XX:XX:XX:XX:XX")
    options = parser.parse_args()
    print(options)
    if options.interfaceArg is None:
        parser.error("[-] not set ethernet interface, use -i in command line.")
    elif options.macArg is None:
        parser.error("[-] not set new MAC address, use -m in command line.")

    return parser.parse_args()


def change_mac(i, m):
    print("---------------------------------------------------")
    print("Old configurations {}:".format(i))
    subprocess.call("ifconfig {}".format(i), shell=True)
    print("---------------------------------------------------")
    print("Down ethernet interface {}...".format(i))
    subprocess.call("ifconfig {} down".format(i), shell=True)
    print("Set new mac address {} to {}".format(m, i))
    subprocess.call("ifconfig {} hw ether {}".format(i, m), shell=True)
    print("Up ethernet interface {}...".format(i))
    subprocess.call("ifconfig {} up".format(i), shell=True)
    print("---------------------------------------------------")
    print("New configurations {}:".format(i))
    subprocess.call("ifconfig {}".format(i), shell=True)


args = check_arguments()
interface = args.interfaceArg
mac = args.macArg

while not validate_interface(interface):
    print("[-] entered invalid ethernet interface: {}".format(interface))
    print("Type valid interface from exist: {}".format(get_interfaces()))
    print("Or type 0 if you want exit")
    interface = input("Interface: ")
    if interface == '0':
        exit()

if mac == 'random':
    mac = get_random_mac()

while not validate_mac(mac):
    print("[-] entered invalid mac address: {}".format(mac))
    print("Type valid mac address like: XX:XX:XX:XX:XX:XX")
    print("Or type 'random' if you want generate random")
    print("Or type 0 if you want exit")
    mac = input("MAC address: ")
    if mac == 'random':
        mac = get_random_mac()
    if mac == '0':
        exit()

change_mac(interface, mac)
