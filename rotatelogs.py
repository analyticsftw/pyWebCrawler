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
    try:
        os.rename(src, dest)
    except:
        print("uh oh")
    finally:
        return True


def compress(file):
    tar = tarfile.open(file + ".gz", "w:gz")
    tar.add(file)
    tar.close()
    return True


pLog = "python.log"
pArchive = date_time + "-" + pLog
pRename = rename(pLog, pArchive, path=path)
if pRename is True:
    compress(path+pArchive)

mLog = "mysql.log"
mArchive = date_time + "-" + mLog
mRename = rename(mLog, pArchive, path=path)
if mRename is True:
    compress(path+mArchive)
