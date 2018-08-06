# -*- utf-8 -*-

import os
import csv

def get_files(dir):
    list = os.listdir(dir)
    flist = []
    for f in list:
        if os.path.isfile(os.path.join(dir, f)):
            flist.append(f)

    return flist


# get dirs but not recusively
def get_dirs(dir):
    list = os.listdir(dir)
    subdirs = []
    for d in list:
        if os.path.isdir(os.path.join(dir, d)):
            subdirs.append(d)

    return subdirs


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
    #result.write("============================================\n")
    #result.write(f + "\n \n")
    res = []
    enc_time = []
    for line in filename.readlines():
        p1 = re.match(
            r"Stream 0 PSNR \(Overall/Avg/Y/U/V\) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3})",
            line) # 3rd step
        p2 = re.search(r"rc_min_quantizer\s+= (\d{2})", line) # 1st step

        p3 = re.match(r"Pass 1/1 frame\s+\d+/\d+\s+\d+B\s+\d+b/f\s+(\d+)b/s\s+\d+\s+ms\s+\((\d+.\d+)\s+fps\)", line) # 2nd step
        p4 = re.match(r"Pass 1/1 frame\s+\d+/\d+\s+\d+B\s+\d+b/f\s+(\d+)b/s\s+\d+\s+ms\s+\((\d+.\d+)\s+fps\)",
                      line)  # 4th step
        if p1:
            # psnr

            # print(p1.group(3), p1.group(4), p1.group(5))
            #result.write(p1.group(3) + ", ")
            #result.write(p1.group(4) + ", ")
            #result.write(p1.group(5) + ", ")
            res.append(p1.group(3) + ", ")
            res.append(p1.group(4) + ", ")
            res.append(p1.group(5) + ", ")
            #result.write("\n" + "\n")
            if len(enc_time) > 0:
                for c in enc_time:
                    res.append(c)

                enc_time = []
        elif p2:
            # qp

            # print("QP = " + p2.group(1))
            #result.write("QP " + ", " + p2.group(1) + "\n")
            res.append(p2.group(1) + ", ")
        elif p3:
            # bitrate fps

            # print(p3.group(0), "kbps="+p3.group(1), p3.group(2))
            #result.write("kbps, " + str(float(p3.group(1)) / 1000) + ", fps," + p3.group(2) + "\n")
            bitrate = float(p3.group(1)) / 1000
            fps = float(p3.group(2))

            enc_s = 1 / fps
            enc_h = enc_s / 3600
            enc_time.append(str(enc_s) + "," + "," + str(enc_h) + "\n")
            #print(fps, enc_s, enc_h)
            res.append(str(bitrate) + ", ")


    for c in res:
        result.write(c)



    #result.write("\n")


    filename.close()




def get_results_v2(result, dir, f):
    print("hello")

    '''
    file = os.path.join(dir, f)
    filename = open(file, "r")
    result.write("============================================\n")
    result.write(f + "\n \n")
    res = []

    for line in filename.readlines():
        p1 = re.match(r"Stream 0 PSNR \(Overall/Avg/Y/U/V\) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3}) (\d{2}\.\d{3})", line)
        p2 = re.search(r"rc_min_quantizer\s+= (\d{2})", line)
        p3 = re.match(r"Pass 1/1 frame\s+\d+/\d+\s+\d+B\s+\d+b/f\s+(\d+)b/s\s+\d+\s+ms\s+\((\d+.\d+)\s+fps\)", line)
        if p1:
            #print(p1.group(3), p1.group(4), p1.group(5))
            #result.write(p1.group(3)+", ")
            #result.write(p1.group(4)+", ")
            #result.write(p1.group(5)+", ")
            res.append(p1.group(3) + ", ")
            res.append(p1.group(4) + ", ")
            res.append(p1.group(5) + "\n")
            #result.write("\n"+"\n")
        elif p2:
            #print("QP = " + p2.group(1))
            #result.write("QP " + ", " + p2.group(1) + "\n")
            res.append(p2.group(1) + ", ")
        elif p3:
            #print(p3.group(0), "kbps="+p3.group(1), p3.group(2))
            #result.write("kbps, " + str(float(p3.group(1)) / 1000) + ", fps," + p3.group(2) + "\n")
            res.append(str(float(p3.group(1)) / 1000) + ", ")

    for c in res:
        result.write(c)

    result.write("\n" + "\n")


    filename.close()
    '''




def is_res_needed(dirs, res):
    for d in dirs:
        p = re.search(res, d)
        if p:
            return d
        else:
            continue

    return None


def files_reorder(flist, order):
    outlist = []

    for p in order:
        for file in flist:
            found = re.search(p, file)
            if found:
                outlist.append(file)
            else:
                continue

    if len(outlist) > 0:
        return outlist
    else:
        return None



import sys

if __name__ == "__main__":

    res_dirs = ["3840x2160", "film", "1920x1080", "1280x720", "832x480", "416x240"]
    uhd = ['Cactus', 'Coastguard', 'Foreman', 'Mobile', 'News', 'pku_girls', 'pku_parkwalk', 'ReadySteadyGo', 'Suzie']
    film = ['Animation', 'Eason', 'King', 'Les', 'lol', 'Run', 'Start', 'Three']
    res_1080 = ['BasketballDrive', 'beach', 'BQTerrace', 'Cactus', 'ColdWar', 'Kimono', 'ParkScene', 'PedestrianArea', 'Sunflower', 'taishan']
    res_720 = ['City', 'Crew', 'FourPeople', 'Harbour', 'Johnny', 'KristenAndSara', 'SlideEditing', 'SlideShow', 'vidyo1', 'vidyo3']
    res_480 = ['BasketballDrill_832x480', 'BasketballDrillText',  'BQMall', 'PartyScene', 'RaceHorses']
    res_240 = ['BasketballPass', 'BlowingBubbles', 'BQSquare', 'RaceHorses']

    dict = {"3840x2160":uhd,
            "film":film,
            "1920x1080":res_1080,
            "1280x720":res_720,
            "832x480":res_480,
            "416x240":res_240}

    if len(sys.argv) == 1:
        print("WRONG CALL!")
        print("python dir")
        dir = r"D:\0-WORK\code\vp9\doc\VP9_TEST_RESULT\AI\real_ai_good"
        result = open(r"D:\0-WORK\code\vp9\doc\VP9_TEST_RESULT\AI\real_ai_good\result.csv", "w")
    else:
        dir = sys.argv[1]
        result = open(dir + "result.csv", "w")

    print("The Results are in a specified order! DO NOT CHANGE\n")
    result.write("CQ-level, kbps, Y psnr, U pnsr, V pnsr, Enc T[s], Dec T[s], Enc[h] \n");

    subdirs = get_dirs(dir)
    #print(subdirs)



    for r in res_dirs:
        d = is_res_needed(subdirs, r)
        if d:
            files = get_files(os.path.join(dir, d))
            flist = classified_by_suffix(files)
            reordered_files = files_reorder(flist, dict[r])
            #print(flist)
            #print(reordered_files)
            for file in reordered_files:
                get_results(result, os.path.join(dir, d), file)



    '''
    dir = r"D:\0-WORK\code\vp9\doc\VP9_TEST_RESULT\LD\LD_good"
    result = open(r"D:\0-WORK\code\vp9\doc\VP9_TEST_RESULT\LD\LD_good\result.txt", "w")
    subdirs = get_dirs(dir)
    print(subdirs)
    if subdirs:
        for d in subdirs:
            result.write("***********************\n")
            result.write("Directtion: " + d + "\n")
            result.write("***********************\n")
            files = get_files(os.path.join(dir, d))
            flist = classified_by_suffix(files)
            for file in flist:
                get_results_v2(result, os.path.join(dir, d), file)
    else:
        files = get_files(dir)
        flist = classified_by_suffix(files)
        for file in flist:
            get_results(result, dir, file)

    
    '''

    result.close()
    print("done!!")

