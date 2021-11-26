#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import datetime
from pyproj import Proj, transform
import plotly.express as px


# In[8]:


pwd = os.getcwd()
filepath = pwd + "/NYPD_Complaint_Data_Historic_Before_Clean.csv" #filepath for dataset

df = pd.read_csv(filepath) #read data into dataframe


# In[10]:


ind = df[df['CMPLNT_FR_DT'].str[-4:-2] == '10'].index #Locate all rows that begin before the year 2000 (removes typos)

df = df.drop(ind).reset_index() #delete rows that begin before the year 2000


# In[11]:


df['CMPLNT_FR_DT'] = pd.to_datetime(df['CMPLNT_FR_DT'],format = '%m/%d/%Y').dt.date #convert to date object

df['CMPLNT_FR_TM'] = pd.to_datetime(df['CMPLNT_FR_TM'],format = '%H:%M:%S').dt.time #convert to time object


# In[12]:


out_of_range_dates = df[(df['CMPLNT_FR_DT'] < datetime.date(2006,1,1)) | (df['CMPLNT_FR_DT'] > datetime.date(2021,1,1))].index #remove any rows that begin before Jan 1 2021

df = df.drop(out_of_range_dates).reset_index()


# In[15]:


cols_to_drop = ['index',
                'Unnamed: 0',
                'level_0',
                'CMPLNT_NUM',
                'CRM_ATPT_CPTD_CD',
                'CMPLNT_TO_DT',
                'CMPLNT_TO_TM',
                'HADEVELOPT',
                'HOUSING_PSA',
                'JURISDICTION_CODE',
                'JURIS_DESC',
                'VIC_AGE_GROUP',
                'VIC_RACE',
                'VIC_SEX',
                'KY_CD',
                'PATROL_BORO',
                'STATION_NAME',
                'TRANSIT_DISTRICT']

df_dropped = df.drop(columns = cols_to_drop) #drop all columns in the list


# In[16]:


from pyproj import Transformer

#Transform state plane coordinates to latitude and longitude
trans = Transformer.from_crs(
    "epsg:2263",
    "epsg:4326",
    always_xy=True,
)
xx, yy = trans.transform(df_dropped['X_COORD_CD'].values, df_dropped['Y_COORD_CD'].values)

#add latitude and longitude values to dataframe
df_dropped["LONGITUDE"] = xx
df_dropped["LATITUDE"] = yy


# In[55]:


px.histogram(df_dropped, x='CMPLNT_FR_DT')


# In[20]:


df_dropped.to_csv('Historic_Cleaned_Data.csv')

