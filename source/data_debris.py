import ephem
import math
import datetime
import os
import numpy as np


def search(x):
    """
    Searches inside the files and parses the lines.

    :param x: name of the file (without tle extension)
    :type x: string

    :return: a list containing all of the lines in the chosen file.
    :rtype: list[str]
    """

    liste = []
    f = open(x + ".tle")
    liste = f.readlines()

    for i in range(len(liste)):
        liste[i] = liste[i].rstrip('\n')
    for i in range(len(liste)):
        liste[i] = liste[i].rstrip()

    return liste


def get_id(ch):
    """
    Gets the ID of the debris from the string containing it
    (first chain of numbers right after the string '2 ' and ending with ' ' in the 2nd line of invidivual TLE )

    :param ch: the string containing the ID
    :type x: string

    :return: the ID
    :rtype: string
    """

    sch = ''
    cha = ch[2:]

    for i in cha:
        if i == ' ':
            break
        sch += i

    return sch


def coordinates(x, time):
    """
    Retrieves the name, id, and the TLE details of all debris from the search function resultant list containing the,
    then creates a list of dictionaries containing the id/name and coordinates of the debris.

    :param x: the list containing the information retrived from the parsing (search function)
    :type x: list[str]

    :param time: the exact date and time in the form year/month/day hours:minutes:seconds
    :type time: string

    :return: the ID, name and the coordinates(altitude,latitude,longitude) at the chosen time
    :rtype: list[dict]
    """

    name = []
    line1 = []
    line2 = []
    identity = []

    for i in range(int(len(x) / 3)):
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
        dictionnaire = dict()
        dictionnaire["id"] = identity[i]
        dictionnaire["name"] = name[i]
        dictionnaire["altitude"] = tle_rec.elevation
        dictionnaire["latitude"] = math.degrees(tle_rec.sublat)
        dictionnaire["longitude"] = math.degrees(tle_rec.sublong)
        liste.append(dictionnaire)

    return liste


def realtime(x):
    """
    Finds coordinates in real time (the Operating system's time)

    :param x: the list containing the information retrived from the parsing (search function)
    :type x:  list[str]

    :return: the ID, name and the coordinates(altitude,latitude,longitude) in real time
    :rtype: list[dict[]]
    """

    now = datetime.datetime.now()
    irt = str(now.year) + '/' + str(now.month) + '/' + str(now.day) + ' ' + str(now.hour) + ':' + str(
        now.minute) + ':' + str(now.second)

    return coordinates(x, irt)


def get_new_time(time):
    """
    Function linked to the time bar in the website, takes the time added or substracted in minutes and modifies the date accordingly.
    While in a new date, the time keeps moving forward.

    :param time: the time change in minutes
    :type time: string

    :return: the new date
    :rtype: string
    """
    plus_time = int(time)

    # graduation is in minutes
    graduation = 8640
    # minutes
    now = datetime.datetime.now()
    plus_time = plus_time * graduation

    m_month = (now.month - 1) * 43200
    m_day = (now.day - 1) * 1440
    m_hour = now.hour * 60
    now_m = m_month + m_day + m_hour + now.minute
    new_m = now_m + plus_time

    now_month = (np.floor(new_m / 43200)) + 1
    now_day = (np.floor((new_m - ((now_month - 1) * 43200)) / 1440)) + 1
    now_hour = np.floor((new_m - ((now_month - 1) * 43200) - ((now_day - 1) * 1440)) / 60)
    now_minute = (new_m - ((now_month - 1) * 43200) - ((now_day - 1) * 1440)) - (now_hour * 60)

    if now_month > 12:
        now_year = now.year + 1
        now_month = now_month - 12
    else:
        now_year = now.year

    nrt = str(int(now_year)) + '/' + str(int(now_month)) + '/' + str(int(now_day)) + ' ' + str(
        int(now_hour)) + ':' + str(
        int(now_minute)) + ':' + str(int(now.second))

    return nrt


def changetime(x, plus_time):
    """
    Finds coordinates after the time change.

    :param x: the list containing the information retrived from the parsing (search function)
    :type x:  list[str]

    :param plus_time: the time change in minutes
    :type plus_time: string

    :return: the ID, name and the coordinates(altitude,latitude,longitude) during the new time
    :rtype: list[dict[]]
    """

    nrt = get_new_time(plus_time)

    return coordinates(x, nrt)


# Categories data base
catbase = [[["Special-Interest Satellites"],
            ["tle-new", "stations", "visual", "active", "analyst", "2019-006", "1999-025", "iridium-33-debris",
             "cosmos-2251-debris"]],
           [["Weather & Earth Resources Satellites"],
            ["weather", "noaa", "goes", "resource", "sarsat", "dmc", "tdrss", "argos", "planet", "spire"]],
           [["Communications Satellites"],
            ["geo", "intelsat", "ses", "iridium", "iridium-NEXT", "starlink", "oneweb", "orbcomm", "globalstar",
             "swarm", "amataeur", "x-comm", "other-comm", "gpz", "gpz-plus"]],
           [["SatNOGS"], ["gorizont", "raduga", "molniya"]],
           [["Navigation Satellites"], ["gnss", "gps-ops", "glo-ops", "galileo", "beidou", "sbas", "nnss", "musson"]],
           [["Scientific Satellites"], ["science", "geodetic", "engineering", "education"]],
           [["Miscellaneous Satellites"], ["military", "radar", "cubesat", "other"]]]


def data_in_dict(param, time):
    """
    Utilizes all the other functions to insert the debris infos in a dictionary for each category.

    :param param: the category (from 0 to 6)
    :type param: string

    :param time: the time stamp on the time bar on the website (if 0 then default state -> real time; if not 0 then there has been a time change)
    :type time: string

    :return: the dictionary containing all of coordinates and IDs
    :rtype: dict
    """

    cat = int(param)
    plus_time = int(time)

    liste = []
    liste_new = []
    dic = dict()

    for i in catbase[cat][1]:
        if os.path.exists(i + ".tle"):
            liste = search(i)
            if plus_time == 0:
                liste_new.extend(realtime(liste))
            else:
                liste_new.extend(changetime(liste, plus_time))
        else:
            continue

    dic = {"coordonnees": liste_new}

    return dic
