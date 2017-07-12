""" This script is designed to assign the diagnosis of for scanned
subjects using their WBIC number based on the diagnosis listed in Query 11
from Julie Wiggins, 9/6/2017"""

import csv
from os import path
from shutil import move

input = "Query11.csv"

f = open(input, "r") # define the input file
root = "/home/tr332/scratch/newDownloads"

reader = csv.DictReader(f, delimiter=",") # read the input file

# define lists of WBIC ID numbers
PSP = []
Control = []

for r in reader:
   if r["Current Diagnosis"] == "Control":
      Control.append(r["WBIC Number"])

   elif r["Current Diagnosis"] == "PSP" or r["Current Diagnosis"]=="PSP-clinical" or r["Current Diagnosis"] == "PAGF/PSP":
      PSP.append(r["WBIC Number"])

print ' '.join(["Control", str(len(Control))])
print ' '.join(Control)

print ' '.join(["PSP", str(len(PSP))])
print ' '.join(PSP)

for c in Control:
   if path.exists(path.join(root, c)):
      print c
      move(path.join(root,c), path.join(root,"Control",c))

for p in PSP:
   if path.exists(path.join(root, p)):
      print p
      move(path.join(root,p), path.join(root,"PSP",p))
