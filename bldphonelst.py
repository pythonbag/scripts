#!/usr/bin/python
#
# extract phone numbers without emails from playerlist
#
import os, sys, getopt, shutil, glob, re, traceback, json, csv
def handle_exception():
#    e = sys.exc_info()[0]
#    print "ERROR:{0}".format(e)
#    traceback.print_stack()
    traceback.print_exc()
    os._exit(1)
def addRow(lst,row):
   key = row[9]
   if key in lst:
      setlst = lst[key]
      setlst.append(row)
   else:
      setlst=[row]
   lst[key]=setlst
   return lst
def addKey(lst,key):
    if key == "":
       return lst
    if key not in lst:
       lst.append(key)
    return lst
def getRow(filename):
    try:
        lst = []
        with open(filename,"rb") as csvfile:
            #rdr = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in rdr:
                hdr=row
                break
            for row in rdr:
                if row[10] == "":
                   if row[11] != "":
                      print row[11]
                if row[65] == "":
                   if row[66] != "":
                      print row[66]
                if row[74] == "":
                   if row[75] != "":
                      print row[75]
                #row=re.sub("\s{2,}" , " ", row)
                #lst=addKey(lst,row[11].lower)
                #lst=addKey(lst,row[66].lower)
                #lst=addKey(lst,row[75].lower)
            csvfile.close()
        return lst
    except:
        traceback.print_exc()
#
# argv[0] = NAME
# argv[1] = IP
#
def main(argv):
    try:
        if len(argv)<1:
           print '{"STATUS":"FAIL", "MSG":"MISSING ARGS" }'
           os._exit(2)
        lst=getRow(argv[0])
#        for key in lst:
#           print key
    except:
        handle_exception()
if __name__ == "__main__":
   main(sys.argv[1:])
