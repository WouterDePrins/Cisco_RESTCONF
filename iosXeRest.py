import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3

# Suppressing warnings for non-secure connection
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IosXeRest(object):

    # The three parameters required for making the connection to the switch
    def __init__(self): 
        self.ip = None
        self.username = None
        self.password = None

    # Create a connection to the switch
    def make_call(self, method, param, payload=""): 
        try:
            return requests.request(method, self.ip + param, auth = HTTPBasicAuth(self.username, self.password), headers = {
                'accept': "application/yang-data+json",
                'content-type': "application/yang-data+json",
            }, verify=False, data=payload)

        except requests.exceptions.Timeout: # If timeout occurs, print message
            print('0h-ooh, connection was not made, time out occured.')

        except requests.exceptions.ConnectionError: # If there is a connection error, print message
            print('Hmm, something went wrong.')

    # Returns all the VLAN's in JSON format (without VLAN 1 & system VLAN's)
    def vlan_get(self):
        return self.make_call('GET', 'vlan/').json()

    # Change VLAN's. This gets the list of all VLAN's first, appends the user input VLAN's and send it back
    # IMPORTANT you get the vlan list first, otherwise you delete all VLAN's and add the one from the user input!
    # Returns True if switch accepted the new VLAN configuration
    
    def vlan_change(self, vlandata):
        vlanlist = self.make_call('GET', 'vlan').json()
        for i in vlandata:
            vlanlist['Cisco-IOS-XE-native:vlan']['Cisco-IOS-XE-vlan:vlan-list'].append(
                {'id': int(i['id']), 'name': i['name']})

        payload = json.dumps(vlanlist)
        if self.make_call('PUT', 'vlan/', payload).status_code == 204:
            return True

    # Return the hostname in JSON format
    def get_hostname(self):
        return self.make_call('GET', 'hostname').json()

    # Sets the hostname and returns True if switch response was OK
    def set_hostname(self, hostname):  # Change HOSTNAME JSON
        payload = json.dumps({"Cisco-IOS-XE-native:hostname": hostname})
        if self.make_call('PUT', 'hostname', payload).status_code == 204:
            return True

# Separates class for user Inpout - separates switch logic
class GuiShell(IosXeRest):
    def user_credentials(self):
        while not self.ip:
            self.ip = input("The IPv4 address of the switch: ")
        self.ip = "https://" + self.ip + "/restconf/data/Cisco-IOS-XE-native:native/"
        while not self.username:
            self.username = input("The username: ")
        while not self.password:
            self.password = input("The password: ")

        return True

    # Print the existing VLANs
    def pretty_get_vlan(self):
        vlan_list = self.vlan_get()
        vlan_list = vlan_list['Cisco-IOS-XE-native:vlan']['Cisco-IOS-XE-vlan:vlan-list']
        if len(vlan_list) == 0:
            print("You don't have any VLAN's configured yet")
        else:
            print("\n You have {} VLAN's configured on the switch: \n".format(len(vlan_list)))
            for i in vlan_list:
                print("VLAN ID {} with name '{}'".format(i['id'], i['name']))

    # Get the hostname of the device
    def pretty_get_hostname(self):
        hostname = self.get_hostname()
        print("The current hostname of the device is '{}'.".format(hostname['Cisco-IOS-XE-native:hostname']))

    # Change the hostname of the device
    def pretty_change_hostname(self):
        hostname = ""
        while hostname == '':
            hostname = input('New hostname: ')
            if self.set_hostname(hostname) is True:
                print("Great, the new hostname is '{}'.".format(hostname))

    # Add new VLANs
    def pretty_change_vlan(self):

        # Get the VLANs first for the users info and validation

        newvlan = []
        vlan_list = self.vlan_get()['Cisco-IOS-XE-native:vlan']['Cisco-IOS-XE-vlan:vlan-list']
        vlan_id = []
        vlan_name = []

        if len((vlan_list)) > 0:
            for i in vlan_list:
                vlan_id.append(i['id'])
                vlan_name.append(i['name'])
            print("You already have VLAN's" ":", ", ".join([str(lst) for lst in vlan_id]))

        # Loop for adding different VLANs
        while True:
            # Loop - validating user VLAN ID
            while True:
                try:
                    user_vlan_id = int(input('VLAN ID: '))
                    if user_vlan_id not in vlan_id:
                        break
                    else:
                        print('Oh-ooh, this VLAN ID is already in use, please take another one.')
                        continue

                except ValueError:
                    print('Only integers are valid for a VLAN ID, try again.')
                    continue

            # Loop - validating user VLAN Name
            while True:
                try:
                    user_vlan_name = str(input('VLAN Name: '))
                    if user_vlan_name not in vlan_name:
                        break
                    else:
                        print('This VLAN name is already in use, provide another name!')
                        print("The names you already used are:", ", ".join([str(lst) for lst in vlan_name]))

                except ValueError:
                    print('Only strings are valid for a VLAN name, try again.')
                    continue

            # Add a new VLAN or break
            newvlan.append({'name': user_vlan_name, 'id': user_vlan_id})
            add_vlan = input('Add another VLAN? (Yes / No): ')
            if 'y' in add_vlan.lower():
                continue
            else:
                break

        # If VLAN's are pushed to the switch, inform user they are added
        if self.vlan_change(newvlan) is True:

            if len(newvlan) == 1:
                print("\nVLAN {} with name '{}' has been added!".format(user_vlan_id, user_vlan_name))
            else:
                print('The following VLANs are added:')
                for i in newvlan:
                    print(" VLAN ID with {} and name '{}'".format(i['id'], i['name']))

    # Python Shell 'GUI'
    def menu(self):
        welcome_into = "Welcome to this basic script for configuring some stuff at a Cisco switch through RESTCONF. \nMake sure you have enabled 'restconf' and 'HTTP enable' on the switch."
        menu_items = " 1. Show the hostname \n 2. Show the VLAN(s) \n 3. Change the hostname \n 4. Create (a) VLAN(s) \n \n Make your choice: "
        print(welcome_into)
        while True:
            input("Press Enter to continue...")
            try:
                choice = int(input('\n' + menu_items))
                if choice == 1:
                    self.pretty_get_hostname()
                if choice == 2:
                    self.pretty_get_vlan()
                if choice == 3:
                    self.pretty_change_hostname()
                if choice == 4:
                    self.pretty_change_vlan()

            except ValueError:
                print('Please provide a number please.')
                continue

# initialisation

a = GuiShell()
if a.user_credentials() is True:
    a.menu()

