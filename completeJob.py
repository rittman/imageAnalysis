from sys import argv
import glob
from os import path,chdir,chmod,system
from shutil import copy

diag = argv[1]

chdir(diag)
dirNames = [v for v in glob.glob("*") if path.isdir(v) ]

copy("../job", "job")
f = open("job","a")
f.writelines("InitialDir = " + "\nQueue\n\nInitialDir = ".join(dirNames) + "\nQueue\n")
f.close()

copy("../wrapper.sh", "wrapper.sh")

system("../distribute.sh")
