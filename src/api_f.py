import numpy as np

def dategood(dates):
    """
    This function converts the date format to python's default date format.
    Args():
    Dates in format DD/MM/YYYY to be converted.
    return:
    List of dates in YYYY-MM-DD
    """
    newdates = []
    for i in dates:
        newdates.append(i[6:10] + "-" + i[3:5] + "-" + i[0:2])
    return newdates

def comtodotandnan(p):
    """
    This takes a list of floats with "," inside a string and returns a new one casted to floats with "." instead of ","
    Args():
    List of strings that contain floats with ","
    return:
    List of floats with "." instead of ","
    """
    ie = []
    for i in p:
        if i=="Ip":
            ie.append(np.nan)
        else:
            ie.append(float(i.replace(",",".")))
    return ie