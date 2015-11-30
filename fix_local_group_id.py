#!/usr/bin/python
#
# fix local group ids
#
import os, sys, getopt, shutil, glob, re, traceback, pwd, grp, platform
from logcmd import logcmd
#
# the system accounts uid<199, /sbin/nologin, and disabled accounts
#
# fo=os.popen("groupdel localIDS")
#
def getUsers(ignore,ignoreShell,minUser,blueTest):
    list = []
    filename="/etc/passwd"
    fo = open(filename,"r")
    for line in fo:
        line=re.sub("\n" , "", line)
        line=re.sub("\r" , "", line)
        #part=re.sub("\s{2,}", " ", line)
        x = line.split(":")
        if len(x) == 7:
            if x[0][0] != "#":
               if x[0] not in ignore:
                   if x[6] not in ignoreShell:
                       uid = int(x[2])
                       if uid > 10000:
                          print "LDAP COLLISION:"+line
#                      if uid >= minUser and ( uid < 9997 or blueTest):
#                          #print "USER:"+x[0]+":"+x[2]
#
# change to don't exclude on range
#
#
                       list.append(x[0])
    fo.close()
    return list
def getLdapUsers(ignore,ignoreShell,minUser,blueTest):
    list = []
    users = pwd.getpwall()
    for u in users:
        if u.pw_name not in ignore:
            if u.pw_uid >= minUser or ( u.pw_uid < 9997 or blueTest):
                if u.pw_shell not in ignoreShell:
                    mylist.append(u.pw_name)
    return list
def main(argv):
    try:
        if len(argv) < 1:
           blueTest = False
        elif "blue" in argv[0]:
           blueTest = True
        else:
           blueTest = False
        if "redhat" in platform.dist()[0]:
            minUser=500
        else:
            minUser=1000
        ignoreShell = ["/sbin/nologin","/bin/false","/sbin/shutdown","/bin/sync","/sbin/halt" ]
        ignore = ["root","adlab","nobody","nagios"]
        mylist = getUsers(ignore,ignoreShell,minUser,blueTest)
        try:
            groupName=grp.getgrnam("localIDS")
            group = groupName[3]
        except KeyError:
            fo=os.popen("groupadd localIDS --gid 9998")
            fo.close()
            group = []
        for user in mylist:
            print "user:"+user
            fo=os.popen("gpasswd -a "+user+" localIDS")
            fo.close()
        for user in group:
            if user not in mylist:
                print "not in group:"
                print user
                try:
                    ingrp=grp.getgrnam(user)
                    fo=os.popen("gpasswd -d "+user+" localIDS")
                    fo.close()
                except KeyError:
                    print "no group for user"
            else:
                print "in group:"+user
    except:
        traceback.print_exc()
if __name__ == "__main__":
   logcmd(sys.argv[0])
   main(sys.argv[1:])
