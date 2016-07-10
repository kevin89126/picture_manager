# -*- coding: Big5 -*- 
from pic import PicManager


def seperate(endwith):
    pm = PicManager(endwith)
    print pm.seperate()

if __name__ == "__main__":
    seperate('.JPG')

