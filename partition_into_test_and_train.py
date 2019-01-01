import os
import shutil
import random
dirs = next(os.walk("dataset/"))[1]
os.mkdir("train")
os.mkdir("test")
for dirr in dirs:
    os.mkdir("train/%s" % (dirr,))
    os.mkdir("test/%s" % (dirr,))
    files = os.listdir("dataset/%s" % (dirr,))
    random.shuffle(files)
    # we keep 75% for training & 25% for test
    train = len(files) * 3 // 4
    for phile in files[:train]:
        shutil.move("dataset/%s/%s" % (dirr,phile), "train/%s/%s" % (dirr,phile))
    for phile in files[train:]:
        shutil.move("dataset/%s/%s" % (dirr,phile), "test/%s/%s" % (dirr,phile))
