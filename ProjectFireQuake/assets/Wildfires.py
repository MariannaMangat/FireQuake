
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
Base = declarative_base()
import pandas as pd
from sqlalchemy import *


# In[13]:


metadata = MetaData()
engine = create_engine('sqlite:///./data/FPA_FOD_20170508.sqlite')
Base.metadata.create_all(engine)


# In[151]:


db_uri = 'sqlite:///./data/FPA_FOD_20170508.sqlite'
engine = create_engine(db_uri)

inspector = inspect(engine)

# Get table information
#print(inspector.get_table_names())

# Get column information
print(inspector.get_columns('Fires'))


# In[17]:


# print (engine.table_names())


# In[22]:


# Get number of records for California per year
# test = engine.execute('SELECT fire_year, count(*) FROM Fires WHERE state == "CA" AND fire_year >= 2014 and fire_size > 1000 GROUP BY fire_year')
# for i in test:
#     print(i)


# In[141]:


# Display first 10 rows
# test = engine.execute('SELECT fire_year, county, fire_size FROM Fires WHERE state == "CA" AND fire_year >= 2010 and fire_year <= 2014 and fire_size > 1000 LIMIT 10')
# for i in test:
#     print(i)


# In[142]:


# Store data in dataframe
df = pd.read_sql('SELECT fire_year,fire_name, fips_name, fips_code, latitude, longitude,DISCOVERY_DATE,CONT_DATE, fire_size FROM Fires WHERE state == "CA" AND fire_year >= 2010 and fire_year <= 2014 and fire_size > 1000 and county <> "none"', engine)


# In[50]:


df


# In[43]:


df.to_csv("fires.csv")


# In[148]:


merge_df = df.rename(index=str,columns={"FIRE_NAME":"Name","FIPS_NAME":"County","FIRE_SIZE":"Acres","FIRE_YEAR":"Year"})
merge_df["Start Date"] = "NaN"
merge_df["Containment Date"] = "NaN"
merge_df.drop(["FIPS_CODE","LATITUDE","LONGITUDE","DISCOVERY_DATE","CONT_DATE"],axis=1,inplace=True)
merge_df = merge_df[["Name","County","Acres","Start Date","Containment Date","Year"]]
merge_df


# In[131]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time


# In[132]:


browser = Browser("chrome", executable_path='chromedriver.exe', headless=True)
# headless - True will not open browser after cell is running


# In[133]:


url = "https://en.wikipedia.org/wiki/2015_California_wildfires"
df_2015_list = pd.read_html(url)
df_2015_clean = df_2015_list[1].columns=df_2015_list[1].iloc[0]
df_2015_clean = df_2015_list[1]
df_2015_clean.drop(0,axis=0,inplace=True)
df_2015_clean.reset_index(inplace=True)
df_2015_clean.drop(["index","Notes","Ref","Km2"],axis=1,inplace=True)
df_2015_clean["Year"] = 2015
df_2015_clean


# In[134]:


url = "https://en.wikipedia.org/wiki/2016_California_wildfires"
df_2016_list = pd.read_html(url)
df_2016_clean = df_2016_list[1].columns=df_2016_list[1].iloc[0]
df_2016_clean = df_2016_list[1]
df_2016_clean.drop(0,axis=0,inplace=True)
df_2016_clean.reset_index(inplace=True)
df_2016_clean.drop(["index","Notes","Ref"],axis=1,inplace=True)
df_2016_clean["Year"] = 2016


# In[135]:


url = "https://en.wikipedia.org/wiki/2017_California_wildfires"
df_2017_list = pd.read_html(url)
df_2017_clean = df_2017_list[4].columns=df_2017_list[4].iloc[0]
df_2017_clean = df_2017_list[4]
df_2017_clean.drop(0,axis=0,inplace=True)
df_2017_clean.reset_index(inplace=True)
df_2017_clean.drop(["index","Notes","Ref"],axis=1,inplace=True)
df_2017_clean["Year"] = 2017
df_2017_clean


# In[138]:


url = "https://en.wikipedia.org/wiki/2018_California_wildfires"
df_2018_list = pd.read_html(url)
df_2018_clean = df_2018_list[5].columns=df_2018_list[5].iloc[0]
df_2018_clean = df_2018_list[5]
df_2018_clean.drop(0,axis=0,inplace=True)
df_2018_clean.reset_index(inplace=True)
df_2018_clean.drop(["index","Notes","Ref","Status"],axis=1,inplace=True)
df_2018_clean["Year"] = 2018
df_2018_clean = df_2018_clean.rename(index=str,columns={"Containment date":"Containment Date","Start date":"Start Date"})
df_2018_clean


# In[149]:


wiki_fire_df = pd.concat([merge_df,df_2015_clean,df_2016_clean,df_2017_clean,df_2018_clean], ignore_index=True)
wiki_fire_df


# In[150]:


engine.dispose()

