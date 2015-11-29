#!/usr/bin/python
#
# ./bldschedule.py ./bracket12.txt ./bracket6.txt  ./u12b4.txt ./u14b2.txt
#
import os, sys, getopt, shutil, glob, re, traceback, json, csv
def handle_exception():
    traceback.print_exc()
    os._exit(1)
def CommentStripper (iterator):
    for line in iterator:
        if line[:1] == '#':
            continue
        if not line.strip ():
            continue
        yield line
def getRow(filename):
    try:
        lst = []
        with open(filename,"rb") as csvfile:
            rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in rdr:
                if not row[0].startswith('#'):
                    lst.append(row)
            csvfile.close()
        return lst
    except:
        traceback.print_exc()
def getOpponent(team,games):
   for idx in range(len(games)):
      if games[idx] == team:
          if ((idx/2)*2) == idx:
             return games[idx+1]
          else:
             return games[idx-1]
   return "BYE"
def isHome(team,games):
   for idx in range(len(games)):
      if games[idx] == team:
          return ((idx/2)*2) == idx
   return false
def minutes(str):
    parts=str.split(":")
    return (60*int(parts[0]))+int(parts[1])
def setSlot(games,schedule,idx,used,team,opp):
    while idx in schedule:
        idx=idx+1
    if isHome(team,games):
       schedule[idx]=[team,opp]
    else:
       schedule[idx]=[opp,team]
    used[team]=1
    used[opp]=1
#
# B2 Saturday 1:00pm+
# B3 Saturday +2 hrs from G1
# B7 Sunday   3:00pm+
# B8 Saturday 3:00pm+
# G1 Saturday 9:00-10:00am
# G2 Saturday work around U12B4 U14B2 schedules
# G3 Saturday 3:00pm+
# G4 Saturday 3:00pm+
#
def mapU10(schedule,u12b4,u14b2,games):
    used={}
    for team in games:
       used[team]=0
    t0=9*60
    t1=minutes(u12b4[0])
    t2=minutes(u14b2[0])
    f1=u12b4[1]
    f2=u14b2[1]
#    if f1=='ho' and f2=='ho':
#       print "close"
#    elif f1 == 'ho' and f2 != 'ho':
#       print "one close"
#    elif f1 != 'ho' and f2 == 'ho':
#       print "one close"
#    else:
#       print "both away"
#       if (t1-t0 > 60) or (t2-t0 > 60):
#          schedule[1]=["G2"]

# G2 Saturday work around U12B4 U14B2 schedules
    opp=getOpponent("G2",games)
    if opp == "G3" or opp == "G4":
       lx=7
    if opp == "G1":
       lx=1
    elif (t0 == t1) or (t0 == t2):
       lx=3
    else:
       lx=7
    setSlot(games,schedule,lx,used,"G2",opp)
# B6 8:00am slot
    if not used["B6"]:
        opp = getOpponent("B6",games)
        if opp != "B7":
           if opp == "B2":
              setSlot(games,schedule,5,used,"B6",opp)
           else:
              setSlot(games,schedule,0,used,"B6",opp)
# B7 Sunday
    if not used["B7"]:
        opp = getOpponent("B7",games)
        setSlot(games,schedule,10,used,"B7",opp)
# G1 Saturday 9:00-10:00am
    opp=getOpponent("G1",games)
    if opp != "G2":
       setSlot(games,schedule,1,used,"G1",opp)
# G3 Saturday 3:00pm+
    if not used["G3"]:
        opp=getOpponent("G3",games)
        if opp != "G1":
           setSlot(games,schedule,7,used,"G3",opp)
# G4 Saturday 3:00pm+
    if not used["G4"]:
        opp=getOpponent("G4",games)
        if opp != "G1":
           setSlot(games,schedule,7,used,"G4",opp)
# B2 Saturday 1:00pm+
    if not used["B2"]:
        opp = getOpponent("B2",games)
        if opp != "B7":
           if lx == 7:
              setSlot(games,schedule,lx-2,used,"B2",opp)
           else:
              setSlot(games,schedule,lx+2,used,"B2",opp)

    if not used["B3"]:
        opp = getOpponent("B3",games)
        if opp != "B7":
           if lx == 7:
              setSlot(games,schedule,lx-2,used,"B3",opp)
           else:
              setSlot(games,schedule,lx+2,used,"B3",opp)
    if not used["B8"]:
        opp = getOpponent("B8",games)
        if opp != "B7":
           setSlot(games,schedule,8,used,"B8",opp)
    for team in games:
       opp = getOpponent(team,games)
       if used[team] == 0:
          for idx in range(9):
             if idx not in schedule:
                setSlot(games,schedule,idx,used,team,opp)
                break
    return schedule
def printSlot(day,time,game):
    print day,time,game[0],"x",game[1]
#
# argv[0] = NAME
# argv[1] = IP
#
def main(argv):
    try:
        if len(argv)<1:
           print '{"STATUS":"FAIL", "MSG":"MISSING ARGS" }'
           os._exit(2)
        #teams={"G1","G2","G3","G4","G5","G6","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12"}
        times=["8:00am","9:00am","10:00am","11:00am","12:00pm","1:00pm","2:00pm","3:00pm","4:00pm","5:00pm","3:00pm"]
        boys=getRow(argv[0])
        girls=getRow(argv[1])
        u12b4=getRow(argv[2])
        u14b2=getRow(argv[3])
        for week in range(len(girls)):
           schedule={}
           games=girls[week]
           games.extend(boys[week])
           print games
           schedule=mapU10(schedule,u12b4[week],u14b2[week],games)
           for slot in range(11):
              if slot in schedule:
                  if slot != 10:
                      printSlot("Sat:",times[slot],schedule[slot])
                  else:
                      printSlot("Sun:",times[slot],schedule[slot])
    except:
        handle_exception()
if __name__ == "__main__":
   main(sys.argv[1:])
