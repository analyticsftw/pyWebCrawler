import os
import tarfile
from datetime import datetime
path = "./logs/"

now = datetime.now()
date_time = now.strftime("%Y-%m-%d")


def rename(src, dest, path='./logs/'):
    src = path + src
    dest = path + dest
    print("Attempting to rename %s to %s" % (src, dest))
    if os._exists(src) is False:
        print("File does not exist")
        return False
    if os._exists(dest) is True:
        print("Rotation log already exists, skipping rename until next rotation")
        return False
    os.rename(src, dest)
    return dest


def compress(file):
    tar = tarfile.open(file + ".gz", "w:gz")
    tar.add(file)
    tar.close()
    return True


pLog = "python.log"
pArchive = date_time + "-" + pLog
pRename = rename(pLog, pArchive)
if pRename is True:
    compress(pRename)

mLog = "mysql.log"
mArchive = date_time + "-" + mLog
mRename = rename(mLog, pArchive)
if mRename is True:
    compress(mRename)
