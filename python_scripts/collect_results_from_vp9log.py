# -*- utf-8 -*-

import os

def get_files(dir):
    list = os.listdir(dir)
    flist = []
    for f in list:
        if os.path.isfile(os.path.join(dir, f)):
            flist.append(f)

    return flist


def classified_by_suffix(flist):
    rlist = []
    for f in flist:
        if f.endswith(".log"):
            rlist.append(f)

    return rlist

import re

def get_results(result, dir, f):
    file = os.path.join(dir, f)
    filename = open(file, "r")
    result.write("============================================\n")
    result.write(f + "\n \n")
    for line in filename.readlines():
        p1 = re.match(r"Stream 0 PSNR \(Overall/Avg/Y/U/V\) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3})", line)
        p2 = re.search(r"rc_min_quantizer\s+= (\d{2})", line)
        p3 = re.match(r"Pass 1/1 frame\s+\d+/\d+\s+\d+B\s+\d+b/f\s+(\d+)b/s\s+\d+\s+ms\s+\((\d+.\d+)\s+fps\)", line)
        if p1:
            #print(p1.group(3), p1.group(4), p1.group(5))
            result.write(p1.group(3)+", ")
            result.write(p1.group(4)+", ")
            result.write(p1.group(5)+", ")
            result.write("\n"+"\n")
        elif p2:
            #print("QP = " + p2.group(1))
            result.write("QP " + ", " + p2.group(1) + "\n")
        elif p3:
            #print(p3.group(0), "kbps="+p3.group(1), p3.group(2))
            result.write("kbps, " + str(float(p3.group(1)) / 1000) + ", fps," + p3.group(2) + "\n")


    filename.close()


if __name__ == "__main__":
    dir = r"F:\tmp\wrkdir"
    files = get_files(dir)
    result = open(r"F:\tmp\wrkdir\result.txt", "w")

    print(files)
    flist = classified_by_suffix(files)
    print(flist)
    for file in flist:
        get_results(result, dir, file)

    result.close()
