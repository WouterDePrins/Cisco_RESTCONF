# Cisco RESTCONF
<h4> Cisco Catalyst 9000 with Python and RESTCONF </h4>
<hr>
<p>
This Python script allows you to communicate with a Cisco Catalyst switch through RESTCONF and Python.
RESTCONF is a new way to configure and automate network devices and supports XML and JSON. </p>
<p>
This basic script is created to show the possibilities what you can do with RESTCONF without touching CLI.
For now,  you can show/change the hostname and show/change/add VLAN's through a Python shell. </p>
<hr>
<strong>Requirements:</strong>
<ul>
  <li> A Cisco Catalyst switch that with an IOS-XE (>= 16.8.1) release </li>
  <li> Python 3 </li>
  <li> Requests (pip3 install requests) </li>
  <li> Enable 'ip http server' and 'restconf' on the switch </li>
</ul>
<hr>
<p>
<strong> Demo </strong>
  </p>

<a href="http://www.youtube.com/watch?feature=player_embedded&v=WJgt-9jenJQ
" target="_blank"><img src="http://img.youtube.com/vi/WJgt-9jenJQ/0.jpg" 
alt="C9K Python RESTCONF" width="240" height="180" border="10" /></a>

<hr>
<h5> This script is only a basic example but imagine the automation you could implement with RESTCONF without using third party stuff... </h5
