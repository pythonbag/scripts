#!/usr/bin/python
#
# convert sportability.com player info to shutterfly.com format.
#
import sys
import csv
def pullContact(list,row,num):
     if row["Parent"+num+"_FirstName"] != "" and row["Parent1_LastName"] != "":
         key=row["Parent"+num+"_FirstName"]+row["Parent1_LastName"]
         if key not in list:
             data = {"FirstName":row["Parent"+num+"_FirstName"],
                "LastName":row["Parent"+num+"_LastName"],
                "HomePhone":row["Phone"],
                "CellPhone":row["Parent"+num+"_Phone"],
                "Email":row["Parent"+num+"_Email"],
                "Address":row["Parent"+num+"_Address"],
                "City":row["Parent"+num+"_City"],
                "State":row["Parent"+num+"_State"],
                "Zip":row["Parent"+num+"_Zip"]}
             list[key]=data
     return list
def csv_reader(filename):
#    with open(filename) as f_obj:
#       reader = csv.DictReader(f_obj, delimiter=',', quotechar='|')
        reader = csv.DictReader(open (filename))
        list = {}
        for row in reader:
            list = pullContact(list,row,"1")
            list = pullContact(list,row,"2")
        print list
if __name__ == "__main__":
    csv_path = "./playersExtended.csv"
    csv_reader(csv_path)
