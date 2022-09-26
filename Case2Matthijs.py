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




df_data = pd.DataFrame(df['data'].values.tolist(), index=df.index)
df2 = pd.concat([df, df_data], axis=1).drop('data', axis=1)
df_data = pd.DataFrame(df2['weather'].values.tolist(), index=df.index) 
df2 = pd.concat([df2, df_data], axis=1).drop('weather', axis=1)

st.title('Dropdown Menu')
st.dataframe(df2)

original_list = ['Frankrijk, Arras', 'Ecuador, Guayaquil']

#original_list = []
#original_list.append (Land("Nederland", 5.6462914, 52.1009166))
#original_list.append (Land("Frankrijk", 2.213749, 46.227638))

result = st.selectbox('Selecteer het land', original_list)
st.write(f'De gekozen plek {result}')

querystring = {"lat":"52.5","lon":"4.8"}

headers = {
 	"X-RapidAPI-Key": "a929aa606bmsh42432cc9b369422p1b8238jsnce8e2abf2f38",
 	"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

tekst = response.json()
df = pd.DataFrame.from_dict(tekst)


print(df2.info())

