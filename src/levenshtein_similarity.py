#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


import transliterate
from transliterate import translit, get_available_language_codes


# In[3]:


#path to data
PATH_TO_DATA = '/media/andrii/earth/Katia/CS_MasterThesis/data/ukwiki/'


# In[4]:


df_red_results = pd.read_csv(PATH_TO_DATA+'uk_red_links_results_lighter.csv', encoding = 'UTF-8',sep='^')


# In[5]:


df_red_results.info()


# In[6]:


df_red_results.head()


# In[7]:


list_of_red_links = df_red_results['red_link_name'].tolist()


# In[8]:


transliterated_rl = []
for redlink in list_of_red_links:
    latinized = translit(redlink, 'uk', reversed=True)
    transliterated_rl.append(latinized)


# In[9]:


transliterated_rl[1]


# In[ ]:





# In[10]:


def extract_list(s):
    return [x.split(',')[1].strip("', ,\"") for x in s[2:-2].split('), (')]


# In[11]:


all_results = {}
all_results_list = [[]] * df_red_results.shape[0]
for i in range(df_red_results.shape[0]):
    if df_red_results['en_similar'][i] == '[]':
        all_results[df_red_results['red_link_name'][i]] = []
        all_results_list[i] = []
    else:
        res = extract_list(df_red_results['en_similar'][i])
        all_results[df_red_results['red_link_name'][i]] = res
        all_results_list[i] = res


# In[12]:


def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


# In[13]:


matched_red_links = []
for row in range(len(transliterated_rl)):
    if all_results_list[row] == []:
        matched_red_links.append('')
    else:
        min_indx = np.argmin(np.array([levenshteinDistance(transliterated_rl[row], x) for x in all_results_list[row]]))
        matched = all_results_list[row][min_indx]
        matched_red_links.append(matched)


# In[14]:


df_matched_red_links = pd.DataFrame({'matched_red_links': matched_red_links})


# In[15]:


df_matched_red_links.head()


# In[20]:


df_red_results = pd.read_csv(PATH_TO_DATA+'ukredlinks_with_ground_truth.csv', encoding = 'UTF-8', sep='^')
df_red_links_with_ground_truth = df_red_results[['red_link_name', 'ground truth']]
uk_red_links_transliteration_results = pd.concat([df_red_links_with_ground_truth, df_matched_red_links], axis=1)


# In[21]:


uk_red_links_transliteration_results.shape


# In[22]:


uk_red_links_transliteration_results.head()


# In[39]:





# In[ ]:





# In[24]:


uk_red_links_transliteration_results = uk_red_links_transliteration_results.apply(lambda x: x.str.strip())
uk_red_links_transliteration_results = uk_red_links_transliteration_results.apply(lambda x: x.str.replace('_', ' '))


# In[27]:


evaluation = []
for row in range(len(df_red_results)):
    if df_red_results['ground truth'][row] == df_red_results['matched_red_links'][row]:
        evaluation.append('TP')
    elif pd.isnull(df_red_results['ground truth'][row]) & pd.isnull(df_red_results['matched_red_links'][row]):
        evaluation.append('TN')
    elif pd.isnull(df_red_results['ground truth'][row]) & pd.notnull(df_red_results['matched_red_links'][row]):
        evaluation.append('FP')
    elif pd.notnull(df_red_results['ground truth'][row]) & pd.isnull(df_red_results['matched_red_links'][row]):
        evaluation.append('FN')
    elif df_red_results['ground truth'][row] != df_red_results['matched_red_links'][row]:
        evaluation.append('FP')


# In[28]:


evaluation = pd.DataFrame({'evaluation': evaluation})


# In[29]:


uk_red_links_transliteration_evaluation = pd.concat([df_red_results, evaluation], axis=1)


# In[33]:


uk_red_links_transliteration_evaluation.head()


# In[34]:


# save results to file
uk_red_links_transliteration_evaluation.to_csv(PATH_TO_DATA+'uk_red_links_transliteration_evaluation.csv', header=True, index=False, encoding = 'UTF-8', sep='^')


# In[ ]:





# In[ ]:




