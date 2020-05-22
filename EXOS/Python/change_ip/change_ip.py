"""
Script        : Switch IP Change
Revision      : 1.0
Last Updated  : 22-May-2020

Purpose       : Change switch IP address and default gateway remotely
Prerequisties : All VLANs created, configured uplink ports with target VLAN
"""
import re

def exos_get_ip(cmd):
    """
    Returns IP configuration for "show conf vlan" or "show conf rtmgr"
    """
    return re.match(
        r".*(?:(?:ipaddress)|(?:default))\s" \
        r"(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}.*)",
        exsh.clicmd(cmd, True)).group(1)

ynchangeip = raw_input("Are you sure you want to re-configure your switch IP configuration now (y/n) [n]: ")
if ynchangeip == "y":
    current_vlan = raw_input("Please enter current VLAN name [Default]: ") or "Default"
    target_vlan = raw_input("Please enter target VLAN name [" + current_vlan + "]: ") or current_vlan
    current_ip = exos_get_ip("show configuration vlan | include \"" + current_vlan + " ipaddress\"")
    target_ip = raw_input("Please enter target switch IP address [" + current_ip + "]: ") or current_ip
    current_gw = exos_get_ip("show configuration rtmgr | include default")
    target_gw = raw_input("Please enter target default gateway IP address [" + current_gw + "]: ") or current_gw
    ynproceed = raw_input("Please check the input. Start the process? (y/n) [y]: ") or "y"
    if ynproceed == "y":
        cmds = ["unconfigure vlan " + current_vlan + " ipaddress",
                "configure vlan " + target_vlan + " ipaddress " + target_ip]
        if current_gw != target_gw:
            cmds.extend(["configure iproute delete default " + current_gw,
                         "configure iproute add default " + target_gw])
        for c in cmds:
            exsh.clicmd(c, False)
    else:
        print "Process aborted"
