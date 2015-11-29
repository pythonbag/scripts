#!/usr/bin/python
#
# convert spreadsheet data, removing multiple spaces
#
import os, sys, getopt, shutil, glob, re, traceback, json, csv
def handle_exception():
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
def getRow(filename):
    try:
        lst = {}
        with open(filename,"rb") as csvfile:
            rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in rdr:
                hdr=row
                break
            for row in rdr:
                row=re.sub("\s{2,}" , " ", row)
                key = row[1].lower()
                if "almaden" in key:
                    lst=addRow(lst,row)
                elif "san jose" in key:
                    lst=addRow(lst,row)
                elif "arc" in key:
                    lst=addRow(lst,row)
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
        for name in lst:
            #print name
            machines=lst[name]
            for machine in machines:
                print machine[9]+","+machine[13]+","+machine[11]+","+machine[12]
                break
            for machine in machines:
                print "        "+machine[3]+","+machine[2]
        #print lst
    except:
        handle_exception()
if __name__ == "__main__":
   main(sys.argv[1:])
