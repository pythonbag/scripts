#!/usr/bin/python
#
# convert sportability.com player info to eayso.org format.
#
import sys
import csv
import re
#
# input header
#
#  0  A League
#  1  B Team
#  2  C PlayerID
#  3  D TeamID
#  4  E LeagueID
#  5  F FirstName
#  6  G LastName
#  7  H Number
#  8  I Position
#  9  J Note
# 10  K Email
# 11  L Phone
# 12  M Captain
# 13  N Rookie
# 14  O Gender
# 15  P Address
# 16  Q City
# 17  R State
# 18  S Zip
# 19  T CustomQ1
# 20  U CustomQ2
# 21  V CustomQ3
# 22  W CustomQ4
# 23  X CustomRestr
# 24  Y ClientQ1
# 25  Z ClientQ2
# 26 AA ClientQ3
# 27 AB ClientQ4
# 28 AC Vol Duty
# 29 AD NrSchool
# 30 AE Team Req
# 31 AF Buddy Req
# 32 AG Conflict
# 33 AH TShirt
# 34 AI Jersey
# 35 AJ Shorts
# 36 AK Birthdate
# 37 AL Age
# 38 AM Grade
# 39 AN Ht
# 40 AO Wt
# 41 AP PdDate
# 42 AQ PdStatus
# 43 AR PdAmt
# 44 AS PdNote
# 45 AT AggID
# 46 AU AggDate
# 47 AV ExpYrs
# 48 AW ExpLeague
# 49 AX ExpSkill
# 50 AY ExpPos
# 51 AZ ExpTeam
# 52 BA LgExp
# 53 BB CurSib
# 54 BC PriorSib
# 55 BD HealthPlan
# 56 BE DoctorName
# 57 BF DoctorPhone
# 58 BG DateAdded
# 59 BH HowAdded
# 60 BI MedNotes
# 61 BJ Notes
# 62 BK Parent1_FirstName
# 63 BL Parent1_LastName
# 64 BM Parent1_Relationship
# 65 BN Parent1_Email
# 66 BO Parent1_Phone
# 67 BP Parent1_Address
# 68 BQ Parent1_City
# 69 BR Parent1_State
# 70 BS Parent1_Zip
# 71 BT Parent2_FirstName
# 72 BU Parent2_LastName
# 73 BV Parent2_Relationship
# 74 BW Parent2_Email
# 75 BX Parent2_Phone
# 76 BY Parent2_Address
# 77 BZ Parent2_City
# 78 CA Parent2_State
# 79 CB Parent2_Zip
# 80 CC Discount_Code1
# 81 CD Discount_Code2
# 82 CE Extras
# 83 CF ReimAmt
# 84 CG ReimDate
# 85 CH ReimCheckNum

def mkPhone(phone):
    phone=re.sub("-","",phone)
    phone=re.sub("\(","",phone)
    phone=re.sub("\)","",phone)
    return phone

def mkRelation(relation):
    if "Father" in relation:
        return "Father"
    if "Mother" in relation:
        return "Mother"
    return ""

def pullContact(row):
    #print row
    for key in row:
        line = re.sub("\s{2,}"," ",row[key])
        line = re.sub("\n{2,}"," ",line)
        line = re.sub("\r{2,}"," ",line)
        row[key] = re.sub(",",":",line)
    data=""+","  #"AYSOID"
    data=data+row["FirstName"]+","  #"FirstName"
    data=data+""+","  #"MI"
    data=data+row["LastName"]+","  #"LastName"
    data=data+""+","  #"Suffix"
    data=data+""+","  #"AKA"
    data=data+row["Address"]+","  #"Street"
    data=data+row["City"]+","  #"City"
    data=data+"CA,"  #"State"
    data=data+row["Zip"]+","  #"Zip"
    if "M" in row["Gender"]:
        data=data+"B,"  #"Gender"
    else:
        data=data+"G,"
    data=data+row["Birthdate"]+","  #"DOB"
    team = row["Team"]
    if "U6" in team:
        div="U-06"
    elif "U8" in team:
        div="U-08"
    elif "U10" in team:
        div = "U-10"
    elif "U12" in team:
        div = "U-12"
    elif "U14" in team:
        div = "U-14"
    else:
        div="U-08"
    data=data+div+","  #"DivisionName"
    data=data+mkPhone(row["Phone"])+","  #"HomePhone"
    data=data+"2014"+","  #"MemberShipYear"
    data=data+mkPhone(row["Phone"])+","  #"EmgPhone"
    data=data+row["Parent1_FirstName"]+" "+row["Parent1_LastName"]+","  #"EmgContact"
    data=data+""+","  #"SchoolName"
    data=data+""+","  #"OneYearRating"
    data=data+""+","  #"TwoYearRating"
    data=data+""+","  #"ThreeYearRating"
    data=data+""+","  #"CurrentRating"
    data=data+""+","  #"NextYearRating"
    data=data+""+","  #"Height"
    data=data+""+","  #"Weight"
    data=data+""+","  #"YearsOfExp"
    data=data+""+","  #"JerseyNumber"
    data=data+""+","  #"UniformSize"
    data=data+""+","  #"JerseySize"
    data=data+""+","  #"ShortsSize"
    data=data+""+","  #"Playsposition"
    data=data+""+","  #"TeamGenderPreference"
    data=data+""+","  #"LocationCode"
    data=data+""+","  #"Isvip"
    data=data+""+","  #"IsHearImp"
    data=data+row["HealthPlan"]+","  #"MedInsCarrier"
    data=data+row["MedNotes"]+","  #"MedicalCondition"
    data=data+row["DoctorName"]+","  #"Doctor"
    data=data+mkPhone(row["DoctorPhone"])+","  #"DoctorPhone"
    data=data+""+","  #"TenderType"
    data=data+""+","  #"CheckDetails"
    data=data+""+","  #"Fee"
    data=data+""+","  #"FeePaid"
    data=data+""+","  #"Balance"
    data=data+row["Parent1_FirstName"]+","  #"PrimaryParentFN"
    data=data+""+","  #"PrimaryParentMI"
    data=data+row["Parent1_LastName"]+","  #"PrimaryParentLN"
    data=data+""+","  #"PrimaryParentSuffix"
    data=data+""+","  #"PrimaryParentAKA"
    data=data+""+","  #"PrimaryParentEmp"
    data=data+""+","  #"PrimaryParentWorkPhone"
    data=data+""+","  #"PrimaryParentWorkphoneExt"
    data=data+row["Parent1_Email"]+","  #"PrimaryParentEmail"
    data=data+row["Parent1_Address"]+","  #"PrimaryParentStreet"
    data=data+row["Parent1_City"]+","  #"PrimaryParentCity"
    data=data+"CA,"  #"PrimaryParentState"
    data=data+row["Parent1_Zip"]+","  #"PrimaryParentZip"
    data=data+""+","  #"PrimaryParentHomephone"
    data=data+mkPhone(row["Parent1_Phone"])+","  #"PrimaryParentCellPhone"
    data=data+row["Parent1_Relationship"]+","  #"PrimaryParentRelationship"
    data=data+row["Parent2_FirstName"]+","  #"SecondaryParentFN"
    data=data+""+","  #"SecondaryParentMI"
    data=data+row["Parent2_LastName"]+","  #"SecondaryParentLN"
    data=data+""+","  #"SecondaryParentSuffix"
    data=data+""+","  #"SecondaryParentAKA"
    data=data+""+","  #"SecondaryParentEmp"
    data=data+""+","  #"SecondaryParentWorkPhone"
    data=data+""+","  #"SecondaryParentWorkphoneExt"
    data=data+row["Parent2_Email"]+","  #"SecondaryParentEmail"
    data=data+row["Parent2_Address"]+","  #"SecondaryParentStreet"
    data=data+row["Parent2_City"]+","  #"SecondaryParentCity"
    if len(row["Parent2_FirstName"]) > 0:
        data=data+"CA,"  #"SecondaryParentState"
    else:
        data=data+","  #"SecondaryParentState"
    data=data+row["Parent2_Zip"]+","  #"SecondaryParentZip"
    data=data+""+","  #"SecondaryParentHomephone"
    data=data+mkPhone(row["Parent2_Phone"])+","  #"SecondaryParentCellPhone"
    relation=mkRelation(row["Parent2_Relationship"])
    data=data+relation+","  #"SecondaryParentRelationship"
    data=data+row["Email"]+","  #"PlayerEmail"
    data=data+","  #"Memo"
    data=data+""+","  #"Remarks"
    data=data+","  #"MailingStreet"
    data=data+","  #"MailingCity"
    data=data+","  #"MailingState"
    data=data+","  #"MailingZip"
    data=data+"Y"+","  #"DOBVerified"
    data=data+"N" #"IsDropped"
    return data
def csv_reader(filename):
#    with open(filename) as f_obj:
#       reader = csv.DictReader(f_obj, delimiter=',', quotechar='|')
        reader = csv.DictReader(open (filename))
        list = {}
        for row in reader:
            data = pullContact(row)
            print data
if __name__ == "__main__":
    csv_path = "./ayso2015fall.csv"
    csv_reader(csv_path)
