
# coding: utf-8

# In[ ]:

import pandas as pd
import time

import sys
sys.path.insert(0, '/media/andrii/earth/Katia/CS_MasterThesis/Red_links_Project_for_Wiki_draft/py')
import functions


# In[ ]:

data_time = '20180920'


# In[ ]:

fn = PATH_TO_DATA_UK+'ukwiki_20180920/20180920-langlinks_uk_en.csv'
df_link = pd.read_csv(fn,  encoding='UTF-8', quotechar='\'')
print(df_link.shape)
print(df_link.columns)


# In[ ]:

EN_ID_NAME = "enwiki-"+data_time+"-id_name.csv"
df_en_name = pd.read_csv(PATH_TO_DATA_EN+'enwiki_20180920/'+EN_ID_NAME, encoding='UTF-8', quotechar="\"", sep='^')
df_en_name = df_en_name[['id','title']]
print(df_en_name.shape)
print(df_en_name.columns)


# In[ ]:

df_link.head()


# In[ ]:

df_en_name.head()


# In[ ]:

# add uk correspondences to en article names
df_en_name = pd.merge(df_en_name, df_link, left_on = 'title', right_on = 'll_title', how = 'left')
df_en_name = df_en_name[['id','title', 'll_from']]
df_en_name.columns = ['id', 'title', 'id_uk']


# In[ ]:

# several en articles have multiple corresponding uk acticles, just remove oldest one uk article
df_en_translated = (df_en_name[~df_en_name['id_uk'].isnull()])[['id', 'id_uk']]
df_en_translated.columns = ['id_en','id_uk']
df_en_translated = df_en_translated.sort_values(by = 'id_en')
df_en_translated = df_en_translated.drop_duplicates(keep = 'first', subset = ['id_uk'])


# In[ ]:




# In[ ]:

# add en correspondences to uk article names


# In[ ]:

fn = PATH_TO_DATA_UK+'ukwiki_20180920/'+"ukwiki-20180920-pages-links.csv.gz"
fn_new = functions.unpack(fn)
df_articles = pd.read_csv(fn_new)


# In[ ]:

df_articles.head()


# In[ ]:

df_uk_name = df_articles.merge(right = df_en_translated, left_on = 'id', right_on = 'id_uk', how = 'left')


# In[ ]:

df_uk_name = df_uk_name[['id','link_val','is_red_link','id_en']]
df_uk_name.columns = ['id','title','is_red_link','id_en']
df_uk_name = df_uk_name.sort_values(by = 'id')


# In[ ]:

df_uk_name.head()


# In[ ]:

df_en_name_.head()


# In[ ]:

# save names to files
df_uk_name.to_csv(PATH_TO_DATA+'uk_names.csv.gz', compression='gzip', header=True, index=False)
df_en_name_.to_csv(PATH_TO_DATA+'en_names.csv.gz', compression='gzip', header=True, index=False)

