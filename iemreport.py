#!/usr/bin/python
#
# process IEM reports to summarize failure counts
#
import os, sys, getopt, shutil, glob, re, traceback, json, csv
def handle_exception():
    traceback.print_exc()
    os._exit(1)
def parseArgs(name):
    try:
        cmd = {}
        itfs = file(name, "r")
        for line in itfs:
            args=line.strip().split('=')
            cmd[args[0]] = args[1]
        itfs.close()
        return cmd
    except IOError:
        cmd["STATUS"]="FAIL"
        cmd["MSG"]="NOFILE"
        return cmd
    except IndexError:
        cmd["STATUS"]="FAIL"
        cmd["MSG"]="FORMAT_ERROR"
        return cmd
    except:
        handle_exception()
def getRow(filename,dump):
    try:
        cnt = 0
        lst = {}
        with open(filename,"rb") as csvfile:
            #rdr = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rdr = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in rdr:
                #row=re.sub("\s{2,}" , " ", row)
                #print row[5]
                if row[5] == "failed":
                    if dump != "":
                       print row
                    if row[1] in lst:
                        lst[row[1]] += 1
                    else:
                        lst[row[1]] = 1
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
        if len(argv)<2:
           dump=""
        else:
           dump=argv[1]
        print "ARGV:",str(argv)
        print "ERR:"+dump
        lst=getRow(argv[0],dump)
        for line in lst:
            print lst[line],",",line
        #print lst
    except:
        handle_exception()
if __name__ == "__main__":
   print "LEN:",len(sys.argv)
   print "ARGV:",str(sys.argv)
   main(sys.argv[1:])
