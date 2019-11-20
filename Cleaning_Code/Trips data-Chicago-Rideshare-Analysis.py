#!/usr/bin/env python
# coding: utf-8

# In[23]:


import csv
import pandas as pd
import numpy as np


# In[24]:


pathfile = "C:\\Users\\Billy\\OneDrive\\Desktop\\Data Engineering class\\Trips.csv"


# In[25]:


infile = open(pathfile,'r')


# In[26]:


reader =pd.read_csv(pathfile,sep=',|;',engine ='python')


# In[27]:


infile.close


# In[73]:


reader.head(20)


# In[28]:


type(reader)


# In[29]:


reader.dtypes


# In[18]:


#Change name

reader.columns=("trip_id",'ride_type_id','start_timestamp','end_timestamp','duration_second','miles','start_census_tract','end_census_tract','start_community_area','end_community_area','fare','tip','extra_charges','trip_total','shared_trip_authorized','start_centroid_latitude','start_centroid_longitude','start_centroid_location','end_centroid_latitude','end_centroid_longitude','end_centroid_location')


# In[40]:


reader.index


# In[30]:


reader.insert(11,'tolls',value='float')
reader.dtypes


# In[22]:


reader.insert(14,'payment_type',value='Series')
reader.dtypes


# In[ ]:




