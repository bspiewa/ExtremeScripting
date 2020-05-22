# Switch IP Change

## Description
Scripts allows user to change switch IP address and default gateway configuration 
(if required) via ssh or telnet. New IP address could be in this same or other VLAN.

### Files
* [change_ip.py](change_ip.py)
* [README.md](README.md)

### Requirements
* Tested on 22.4.1.4-patch1-3
* Platform(s): Any ExtremeXOS switch

## Example
```
X460-G2-48t-10GE4 # run script change_ip.py
Are you sure you want to re-configure your switch IP configuration now (y/n) [n]: y
Please enter current VLAN name [Default]:
Please enter target VLAN name [Default]: VLAN_12
Please enter target switch IP address [10.100.1.27 255.255.0.0]: 10.12.1.27 255.255.255.0
Please enter target default gateway IP address [10.100.10.2]: 10.12.1.1
Please check the input. Start the process? (y/n) [y]:
<--- remote session disconnects here --->
```
## Notes
* Check VLAN names and uplink configuration for target VLAN before running the 
script
* To make it easier script provides in prompts as default values data from VLAN 
entered as "current VLAN" and configured in switch default gateway (if any exists)

Tips:
* Please re-login to switch after IP change to save switch new configuration
* You can schedule switch reboot ("reboot time ...") before executing the script 
- if something go wrong and you won't be able to contact your switch using its new IP
then your switch will restart at scheduled time with saved config. If everything 
be fine then after successfull re-login you need only to run command "reboot cancel" 
to cancel scheduled reboot.

## License
Copyright© 2015, Extreme Networks.  All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
The software is provided as is and Extreme Networks has no obligation to provide
maintenance, support, updates, enhancements or modifications.
Any support provided by Extreme Networks is at its sole discretion.

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).

>Be Extreme
