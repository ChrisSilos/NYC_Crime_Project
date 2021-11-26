#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[28]:


current_year_data = pd.read_csv(os.getcwd() + '/Current_Year_Cleaned_Data.csv')

current_year_data.rename(columns = {'Unnamed: 0':'Index'},inplace = True)
current_year_data.set_index(['Index'],inplace = True)


# In[29]:


historic_data = pd.read_csv(os.getcwd() + '/Historic_Cleaned_Data.csv')

historic_data.rename(columns = {'Unnamed: 0':'Index'},inplace = True)
historic_data.set_index(['Index'],inplace = True)


# In[33]:


frames = [historic_data,current_year_data]


# In[34]:


final_data = pd.concat(frames)


# In[40]:


final_data.to_csv('NYC_Complaint_Data_All_Years_Cleaned.csv')

