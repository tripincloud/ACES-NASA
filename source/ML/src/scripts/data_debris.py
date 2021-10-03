import ephem
import math
import datetime
import os 

def search(x):
    liste=[]
    f = open(x + ".tle")
    liste = f.readlines()
    for i in range(len(liste)):
        liste[i] = liste[i].rstrip('\n')
    for i in range(len(liste)):
        liste[i] = liste[i].rstrip()
    return liste

#2 49122  98.2820 345.6698 0001582 159.7763 200.3500 14.57684755  3548
def get_id(ch):
    sch = ''
    cha = ch[2:]
    for i in cha:
        if i==' ':
            break
        sch += i
    return sch



def coordinates(x,time):

    name = []
    line1 = []
    line2 = []
    identity = []
    for i in range(int(len(x)/3)):
        name.append(x[0])
        line1.append(x[1])
        line2.append(x[2]) 
        identity.append(get_id(x[2]))
        x.remove(x[0])
        x.remove(x[0])
        x.remove(x[0])


    liste = []
    
    for i in range(len(name)):
        tle_rec = ephem.readtle(name[i], line1[i], line2[i])
        tle_rec.compute(time)
        #print(name[i],tle_rec.sublong, tle_rec.sublat, tle_rec.elevation)
        dictionnaire = dict()
        dictionnaire["id"] = identity[i]
        dictionnaire["name"] = name[i]
        dictionnaire["altitude"] = tle_rec.elevation
        dictionnaire["latitude"] = math.degrees(tle_rec.sublat)
        dictionnaire["longitude"] = math.degrees(tle_rec.sublong)
        liste.append(dictionnaire)

    return liste

def realtime(x):
    now = datetime.datetime.now()
    irt = str(now.year) + '/' + str(now.month) + '/' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) 
    return coordinates(x,irt)


        



catbase = [[["Special-Interest Satellites"],["tle-new","stations", "visual", "active", "analyst", "2019-006", "1999-025", "iridium-33-debris", "cosmos-2251-debris"]],  
    [["Weather & Earth Resources Satellites"],["weather","noaa","goes","resource","sarsat","dmc","tdrss","argos","planet","spire"]],
    [["Communications Satellites"],["geo","intelsat","ses","iridium","iridium-NEXT","starlink","oneweb","orbcomm","globalstar","swarm","amataeur","x-comm","other-comm","gpz","gpz-plus"]],
    [["SatNOGS"],["gorizont","raduga","molniya"]],
    [["Navigation Satellites"],["gnss","gps-ops","glo-ops","galileo","beidou","sbas","nnss","musson"]],
    [["Scientific Satellites"],["science","geodetic","engineering","education"]],
    [["Miscellaneous Satellites"],["military","radar","cubesat","other"]],
    [["All"],["tle-new","stations", "visual", "active", "analyst", "2019-006", "1999-025", "iridium-33-debris", "cosmos-2251-debris","weather","noaa","goes","resource","sarsat","dmc","tdrss","argos","planet","spire","geo","intelsat","ses","iridium","iridium-NEXT","starlink","oneweb","orbcomm","globalstar","swarm","amataeur","x-comm","other-comm","gpz","gpz-plus","gorizont","raduga","molniya","gnss","gps-ops","glo-ops","galileo","beidou","sbas","nnss","musson","science","geodetic","engineering","education","military","radar","cubesat","other"]]]  


category = int(input("Category: "))

def data_in_dict():
    liste=[]
    liste_new = []
    dic = dict()
    for i in catbase[category][1]:
        if os.path.exists(i + ".tle"):
            liste = search(i)
            liste_new.extend(realtime(liste))
        else:
            continue

    dic = {"coordonnees": liste_new}
    return dic



def data_in_list():
    liste=[]
    liste_new = []
    dic = dict()
    for i in catbase[category][1]:
        if os.path.exists(i + ".tle"):
            liste = search(i)
            liste_new.extend(realtime(liste))
        else:
            continue
    return liste_new
