import subprocess
import os
import shutil
import random
dirs = next(os.walk("train/"))[1]
for dirr in dirs:
    for tt in ["test", "train"]:
        ipt = "%s/%s" % (tt, dirr,)
        files = [x for x in os.listdir(ipt) if x[-4:] == ".png"]
        for phile in files:
            subprocess.call("convert %s %s" % ("%s/%s" % (ipt, phile), "%s/%s" % (ipt, phile[-4:] + ".jpg")), shell=True)
            os.remove("%s/%s" % (ipt, phile))
