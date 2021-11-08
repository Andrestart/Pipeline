import numpy as np

def dategood(dates):
    newdates = []
    for i in dates:
        newdates.append(i[6:10] + "-" + i[3:5] + "-" + i[0:2])
    return newdates

def comtodotandnan(p):
    ie = []
    for i in p:
        if i=="Ip":
            ie.append(np.nan)
        else:
            ie.append(float(i.replace(",",".")))
    return ie