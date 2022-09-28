# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 10:59:09 2022

@author: matthijs
"""

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go

#import plotly.express as px

import datetime as dt
from dateutil.relativedelta import relativedelta # to add days or years

import plotly.io as pio
pio.renderers.default = 'browser'


class Land:
  def __init__ (self, land, latitude, longitude):
    self.land = land
    self.longitude = longitude
    self.latitude = latitude
    def show_all(self):
        print (self.land, self.latitude, self.longitude)

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly"


headers = {
  "X-RapidAPI-Key":"f63be25ec8msh09be29d15fcc4fbp1f0f6ejsn82d64b7f3674",
 	#"X-RapidAPI-Key": "a929aa606bmsh42432cc9b369422p1b8238jsnce8e2abf2f38",
 	"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}

combo_list=[]
original_list = []
combo_list.append(Land("Arras, Frankrijk", 50.292000, 2.780000))
combo_list.append(Land("Guayaquil, Ecuador",-2.203816 ,-79.897453))
combo_list.append(Land("Buenaventura, Colombia", 3.8801, -77.0312))
combo_list.append(Land("Aomorishi, Japan", 40.650497398, 140.850163266 ))
combo_list.append(Land("Manhattan, New York, VS", 40.776676, -73.971321))
combo_list.append(Land("Amsterdam, Nederland", 52.377956, 4.897070))
combo_list.append(Land("Rome, Italië", 41.902782, 12.496366))
combo_list.append(Land("Stockholm, Zweden", 59.334591, 18.063240))

for obj in combo_list:
  original_list.append(obj.land)

result = st.sidebar.selectbox('Selecteer het land', original_list)

for obj in combo_list:
   if (result == obj.land):
      querystring = {"lat": obj.latitude,"lon":obj.longitude}

response = requests.request("GET", url, headers=headers, params=querystring)
tekst = response.json()
df = pd.DataFrame.from_dict(tekst)



#dictionaries opsplitten
df_data = pd.DataFrame(df['data'].values.tolist(), index=df.index)
df2 = pd.concat([df, df_data], axis=1).drop('data', axis=1)
df_data = pd.DataFrame(df2['weather'].values.tolist(), index=df.index) 
df2 = pd.concat([df2, df_data], axis=1).drop('weather', axis=1)

st.title('Weer met 3 uur interval')
df2['datetime']= pd.to_datetime(df2['datetime'], format='%Y-%m-%d:%H')


# put all widgets in sidebar and have a subtitle
with st.sidebar:
    st.subheader('Configure the plot')
    #widget to choose which variable to display
    check1 = st.checkbox ("Temperature")
    check2 = st.checkbox ("UV")           
    check3 = st.checkbox ("Snow") 
    
    #sliders
    cols1,_ = st.columns((15,3)) # To make it narrower
    format2 = 'MMM DD' # format output
    start_date = min(df2['datetime']).date()#  I need some range in the past
    end_date = max(df2['datetime']).date()
    max_days = end_date-start_date
    slider = cols1.slider('Select date', min_value=start_date, value=(start_date,end_date) ,max_value=end_date, format=format2)
    slider_begin = slider[0]
    slider_einde =  slider[1]                                  


#oude line plot
#st.line_chart(data=df2, x='datetime', y='temp', width=0, height=0, use_container_width=True)


#datums filteren
df2['day'] = df2['datetime'].dt.date
df2 = df2[(df2['day'] >= slider_begin) & (df2['day'] <= slider_einde)]

fig = go.Figure(go.Scatter(x = df2['datetime'], y = df2['temp'], mode = 'lines'))
st.plotly_chart(fig)


