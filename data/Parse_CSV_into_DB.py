#!/usr/bin/env python
# coding: utf-8

# In[53]:


import pandas as pd
import math
filename = 'Beautiful adhkar.csv'
df = pd.read_csv(filename)
# df.head()


# In[54]:


df.head()


# In[73]:


import sqlite3
import os

# Create a SQL connection to our SQLite database
con = sqlite3.connect(os.path.join("..","dataentry.sqlite3"))

cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM adhkar;'):
    print(row)


# In[74]:


for index, row in df.iterrows():
    shortDesc = row['shortDescription']
    search = (shortDesc,) #https://docs.python.org/2/library/sqlite3.html
    cur.execute('SELECT * FROM adhkar WHERE shortDescription=?', search)
    db_result = cur.fetchone()
    if(db_result):
        print('already_found:',db_result)
    else:
        print('not found:',search)
        seconds = row['secondsToRecite']
        minutes = row['minutesToRecite']
        
        if(math.isnan(minutes) or math.isnan(seconds)):
            if(math.isnan(minutes) and math.isnan(seconds)):
                continue;
            if(math.isnan(minutes)):
                minutes = seconds / 60
            if(math.isnan(seconds)):
                seconds = minute * 60

                
        seconds = int(seconds)
        minutes = int(minutes)
        
        adhkar_row = (row['arabic'], row['english'], seconds, minutes, row['shortDescription'])
        
        cur.execute("INSERT INTO adhkar (arabic, english, secondsToRecite, minutesToRecite, shortDescription) VALUES (?,?,?,?,?)", adhkar_row)
        # could batch these up and do them at the end 
        # but if we do it per-row it avoids duplicates in the same file. 
        # so it's better todo it per-row.
        
for row in cur.execute('SELECT * FROM adhkar;'):
    print(row)


# In[71]:


con.commit()
con.close()


# In[ ]:





# In[ ]:





# In[ ]:




