#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import pandas as pd
import numpy as np


# In[33]:


traffic_df_old = pd.read_csv("Chicago_Traffic_2011-2018.csv", nrows = 2000)


# In[65]:


traffic_df_old.head()


# In[67]:


traffic_df_old.dtypes


# In[61]:


# Change names
traffic_df_old.columns = ["timestamp_id", "segment_id", "bus_count", "gps_pings", "speed"]

# Change datetime
pd.to_datetime(traffic_df_old.timestamp_id)

# Add columns
def speed_condition(c):
  if c['speed'] < 10:
    return 'slow'
  elif 10 <= c['speed'] < 20:
    return 'medium'
  elif c['speed'] >= 20:
    return 'regular'
  else:
    return 'undefined'

traffic_df_old["speed_category"] = traffic_df_old.apply(speed_condition, axis = 1)

traffic_df_old["comments"] = ""


# In[64]:


pd.to_datetime(traffic_df_old.timestamp_id)


# In[ ]:





# In[44]:





# In[ ]:




