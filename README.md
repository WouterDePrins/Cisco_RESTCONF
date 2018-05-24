# Cisco RESTCONF
Cisco Catalyst 9000 - RESTCONF

This simple script allows you to communicate with a Cisco Catalyst switch through RESTCONF and Python.
RESTCONF is a new way to configure and automate network devices and supports XML and JSON.

This basic script is created to show how to configure a switch without touching the CLI.
For now,  you can show/change the hostname and show/change/add VLAN's through a Python shell.

Requirements:
A Cisco Catalyst switch that with an IOS-XE (>= 16.8.1) release

Python version >= 3
Requests (pip3 install requests)

Enable 'ip http server' and 'restconf' on the switch and you're ready to go.
