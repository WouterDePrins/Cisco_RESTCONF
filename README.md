# Cisco RESTCONF
Cisco Catalyst 9000 - RESTCONF

This simple script allows you to communicate with a Cisco Catalyst switch through RESTCONF and Python.
RESTCONF is a new way to configure and automate network devices and supports XML and JSON.

For now, this script only communicates with one switch and does not really involve automation. It's just a way to show how you can do HTTP GET/PUT/DELETE commands towards the Cat9K switch.

Requirements:
A Cisco Catalyst switch that with an IOS-XE release that supports RESTCONF
Enable 'ip http server' and 'restconf' on the switch.



