# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 19:02:30 2022

@author: matth
"""


import pandas as pd
import requests
import streamlit as st

class Land:
  def __init__ (self, land, longitude, latitude):
    self.land = land
    self.longitude = longitude
    self.latitude = latitude
    
  def show_all(self):
    print (self.land, self.longitude, self.latitude)

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly"



headers = {
 "X-RapidAPI-Key":"f63be25ec8msh09be29d15fcc4fbp1f0f6ejsn82d64b7f3674",
 	#"X-RapidAPI-Key": "a929aa606bmsh42432cc9b369422p1b8238jsnce8e2abf2f38",
 	"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}


combo_list=[]
original_list = []
combo_list.append(Land("Frankrijk, Arras", 2.77, 50.29))
combo_list.append(Land("Ecuador, Guayaquil", -79.89, -2.20))
combo_list.append(Land("Turkije, Ankara", 32.85, 39.93))

for obj in combo_list:
  original_list.append(obj.land)



result = st.selectbox('Selecteer het land', original_list)
st.write(f'De gekozen plek {result}')

for obj in combo_list:
   if (result == obj.land):
      querystring = {"lat": obj.latitude,"lon":obj.longitude}

st.write(f'{querystring}')

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)
tekst = response.json()

df = pd.DataFrame.from_dict(tekst)


df_data = pd.DataFrame(df['data'].values.tolist(), index=df.index)
df2 = pd.concat([df, df_data], axis=1).drop('data', axis=1)
df_data = pd.DataFrame(df2['weather'].values.tolist(), index=df.index) 
df2 = pd.concat([df2, df_data], axis=1).drop('weather', axis=1)

st.dataframe(df2)


print(df2.info())

