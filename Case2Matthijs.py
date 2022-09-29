# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 10:59:09 2022

@author: matth
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

class icon:
  def __init__ (self, icon, description):
    self.icon = icon
    self.description = description
    def show_all(self):
        print (self.icon, self.description)


st.set_page_config(layout = 'wide')

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/3hourly"

headers = {
 "X-RapidAPI-Key":"f63be25ec8msh09be29d15fcc4fbp1f0f6ejsn82d64b7f3674",
 	#"X-RapidAPI-Key": "a929aa606bmsh42432cc9b369422p1b8238jsnce8e2abf2f38",
 	"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"}

combo_list=[]
original_list = []
combo_list.append(Land("Arras, France", 50.292000, 2.780000))
combo_list.append(Land("Guayaquil, Ecuador",-2.203816 ,-79.897453))
combo_list.append(Land("Buenaventura, Colombia", 3.8801, -77.0312))
combo_list.append(Land("Aomorishi, Japan", 40.650497398, 140.850163266 ))
combo_list.append(Land("Manhattan, New York, USA", 40.776676, -73.971321))
combo_list.append(Land("Amsterdam, The Netherlands", 52.377956, 4.897070))
combo_list.append(Land("Rome, Italy", 41.902782, 12.496366))
combo_list.append(Land("Stockholm, Sweden", 59.334591, 18.063240))

for obj in combo_list:
  original_list.append(obj.land)

#radio
result = st.sidebar.radio('Select the city', original_list)

for obj in combo_list:
    if (result == obj.land):
      querystring = {"lat": obj.latitude,"lon":obj.longitude}



response = requests.request("GET", url, headers=headers, params=querystring)
tekst = response.json()
df = pd.DataFrame.from_dict(tekst)

df_data = pd.DataFrame(df['data'].values.tolist(), index=df.index)
df2 = pd.concat([df, df_data], axis=1).drop('data', axis=1)
df_data = pd.DataFrame(df2['weather'].values.tolist(), index=df.index) 
df2 = pd.concat([df2, df_data], axis=1).drop('weather', axis=1)




st.title('Weather with 3 hour interval')
df2['datetime']= pd.to_datetime(df2['datetime'], format='%Y-%m-%d:%H')


# put all widgets in sidebar and have a subtitle
with st.sidebar:
   
    #slider
    cols1,_ = st.columns((15,3)) # To make it narrower
    format2 = 'MMM DD' # format output
    start_date = min(df2['datetime']).date()#  I need some range in the past
    end_date = max(df2['datetime']).date()
    max_days = end_date-start_date
    slider = cols1.slider('Date',min_value=start_date, value=(start_date,end_date) ,max_value=end_date, format=format2)
    slider_begin = slider[0]
    slider_einde =  slider[1] 
    
    #selectbox
    var_name = st.selectbox('Kind of variable', ['Temperature', 'Windspeed', 'Precipitation', 'Snow','UV',  'DHI', ])
    var_name_dict = {"Temperature":'temp','UV':'uv', 'Snow': 'snow', 'DHI':'dhi', 'Windspeed' : 'wind_spd', 'Precipitation':'precip'}
         
      

col1, col2 = st.columns([7,4])

with col2:               
    st.markdown('**Current temperature: ' + str(df2['temp'].iloc[0]) + '**')
    st.markdown('**Current wind direction: ' + str(df2['wind_cdir'].iloc[0]) + '**')
    
    i = df2['description'].iloc[0]
    st.markdown('**Current weather: ' + i + '**')
    
    #icon weather 
    if i == 'Broken clouds':
        st.image("https://www.weatherbit.io/static/img/icons/c03d.png")
    elif i == 'Clear Sky':
        st.image("https://www.weatherbit.io/static/img/icons/c01d.png")
    elif i == 'Drizzle':
        st.image("https://www.weatherbit.io/static/img/icons/d02d.png")
    elif i == 'Few clouds':
        st.image("https://www.weatherbit.io/static/img/icons/c02d.png")
    elif i == 'Fog':
        st.image("https://www.weatherbit.io/static/img/icons/a05d.png")
    elif i == 'Light rain':
        st.image("https://www.weatherbit.io/static/img/icons/r01d.png")
    elif i == 'Light shower rain':
        st.image( "https://www.weatherbit.io/static/img/icons/r04d.png")
    elif i == 'Moderate rain':
         st.image("https://www.weatherbit.io/static/img/icons/r02d.png")
    elif i == 'Overcast clouds':
        st.image( "https://www.weatherbit.io/static/img/icons/c04d.png")
    elif i == 'Scattered clouds':
        st.image("https://www.weatherbit.io/static/img/icons/c02d.png")
    elif i == 'Shower rain':
        st.image("https://www.weatherbit.io/static/img/icons/r05d.png")
    elif i == "Thunderstorm with heavy rain":
        st.image("https://www.weatherbit.io/static/img/icons/t03d.png")
    elif i == "Thunderstorm with rain":
        st.image("https://www.weatherbit.io/static/img/icons/t02d.png")
    else:
        st.image("https://cdn.icon-icons.com/icons2/1659/PNG/512/3844446-cloud-computing-data-disable-off-server-unavailable_110295.png")

    

#datums filteren
df2['day'] = df2['datetime'].dt.date
df2 = df2[(df2['day'] >= slider_begin) & (df2['day'] <= slider_einde)]

#oude line plot
#st.line_chart(data=df2, x='datetime', y='temp', width=0, height=0, use_container_width=True)

with col1:
    
    fig = go.Figure(go.Scatter(x = df2['datetime'], y = df2[var_name_dict[var_name]], mode = 'lines'))
    
    fig.update_layout(title_text = (var_name + ' in ' + result), 
                      font = dict(size = 18), title = dict(y = 0.9, x = 0.5, xanchor = 'center', yanchor = 'top'))
    fig.update_xaxes(title_text = "Date") 
    fig.update_yaxes(title_text = var_name)
    
    st.plotly_chart(fig)

print(df2.info())
