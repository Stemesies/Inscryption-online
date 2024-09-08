import os
from os import rename, listdir
from os.path import isfile, join

mypath = "C:\\Files\\MyProjects\\Programms\\PyCharm\\Insctyprion\\assets\\textures\\cards\\sigils\\"
files = [f for f in listdir(mypath)]
for i in files:
    if "ability" in i:
        os.rename(mypath+i, mypath+i.replace("ability_", "").replace("pixel", ""))
        print(i.replace("pixel", ""))