import numpy as np
import pandas as pd
import requests
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import os
import src.api_f as fapi

#Getting data showing accidents in Madrid in 2020

ac = pd.read_csv('data/2020_Accidentalidad.csv', sep=';')

#The dataset has a register per person involved in an accident.
#As I'd like to get the total number of accidents per day, I got the data from the colunmn "num_expediente",
# which is the accident id, being different in every accident. 
#Because of that, I am removing the duplicates in that column.
ac = pd.DataFrame(ac)
ac.drop_duplicates(subset='num_expediente',inplace=True)

#I am creating a new dataset extracting only the columns 'fecha' and 'num_expediente'.
newac = pd.DataFrame(ac[['fecha','num_expediente']])

#I'm going to change the date format to the one by default in Python (YYYY-MM-DD) using my "dategood" function.
"""def dategood(dates):
    newdates = []
    for i in dates:
        newdates.append(i[6:10] + "-" + i[3:5] + "-" + i[0:2])
    return newdates"""

newac.fecha = fapi.dategood(newac.fecha)

#I am creating a new column named "numacc" that will show the number of accidents per day.
newac['numacc'] = newac.groupby('fecha')['fecha'].transform('count')

#Sorting the dataset by its date and deleting the duplicate values in the column 'fecha'.
newac = newac.sort_values(by='fecha')
newac.drop_duplicates(subset='fecha', inplace=True)

#The index changed after doing the previous adjustments, so I decide to reset it.
newac.reset_index(drop=True, inplace=True)

#Exporting the dataframe I created in a folder named "new_dataframes".
if not os.path.exists("new_dataframes"):
    os.mkdir("new_dataframes")

newac.to_csv('new_dataframes/newac.csv')

##
##Getting some  more  data from  AEMET api.
##
json = pd.io.json.read_json(path_or_buf='data/opendata.aemet.es.json', orient='index')
urljson = json[0]['datos']

#You can see below the real request I made to get the data from the json, but they only allow each request for 5 minutes, 
#so I decided to save the dataset I got in the file "dataframe_aemet.csv"
"""
#res2 = requests.get(urljson)
#datos = res2.json()
#dfaemet = pd.DataFrame(datos)
#dfaemet.to_csv(r'../data/dataframe_aemet')
"""
dfaemet = pd.read_csv('data/dataframe_aemet.csv')

#The columns I am interested in are "fecha" and "prec", as I'd like to know how much it rained per day in Madrid. 
#The date is already in Python date format by default, but the prec data are expressed floats in a string
#separated by commas. Because of that, I am going to cast them in floats and replace the comma for a dot.
#Apart from that, there is a value that is not a float, but a string ("Ip"), so will create a NaN instead.
#I will use my function "comtodotandnan".

dfaemet.prec = fapi.comtodotandnan(dfaemet.prec)

#I am creating a new dataframe with the columns "fecha" and "prec".
dfprec = dfaemet[['fecha','prec']]

#In order to join both dataframes and be able to make a new dataframe with all data I'm interested in,
#I am first creating a new one with only one column that will show the number of accidents per day,
# already ordered by date.
numacc = pd.DataFrame(newac.numacc)

#I am going to use that dataframe to join it with the one I had. I will call it "finaldf.csv" and will save it.
dffinal = dfprec.join(newac.numacc)
dffinal.to_csv('new_dataframes/finaldf.csv')

#########################################
#############Creating graphs#############
#########################################
#I am making a correlation table mixing the number of accidents and rain fallen per day.
if not os.path.exists("graphs"):
    os.mkdir("graphs")

cor = dffinal.corr()
cor.to_csv('new_dataframes/cor.csv')

#Scatter plot
scatacrain = px.scatter(dffinal, x="numacc", y="prec", width = 1000, height = 330)
#scatacrain.write_image('graphs/scatacrain.png')

#Scatter matrix
scatmatr = px.scatter_matrix(dffinal)
#scatmatr.write_image('graphs/scatmatr.png')

#Rain per day in violin plot
viorain = go.Figure(data=go.Violin(x=dffinal.prec, box_visible=True, line_color='black',
                               meanline_visible=True, fillcolor='cornflowerblue', opacity=0.8,
                               points="all", name='Rain per day in Madrid'))
#viorain.write_image('graphs/viorain.png')

#Accidents per day in violin plot
vioac = go.Figure(data=go.Violin(x=dffinal.numacc, box_visible=True, line_color='black',
                               meanline_visible=True, fillcolor='indianred', opacity=0.8,
                                 points="all", name='Accidents per day in Madrid'))
#vioac.write_image('graphs/vioac.png')

#Rain per day in mm/m2
rain = px.bar(newac, x='fecha', y='numacc')
#rain.write_image('graphs/rain.png')

#Accidents per day in barplot
acc = px.bar(dffinal, x='fecha', y='prec')
#acc.write_image('graphs/acc.png')
