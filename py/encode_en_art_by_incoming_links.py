import pandas as pd
import numpy as np
import progressbar

import sys
sys.path.insert(0, '/media/andrii/earth/Katia/CS_MasterThesis/Red_links_Project_for_Wiki_draft/py')
import functions

#path to data
PATH_TO_DATA = '/media/andrii/earth/Katia/CS_MasterThesis/data/'
PATH_TO_DATA_UK = PATH_TO_DATA+"ukwiki/"
PATH_TO_DATA_EN = PATH_TO_DATA+"enwiki/"

data_time = '20180920'

# load a table with English titles with their ids and uk correspondences
df_en_name = pd.read_csv(PATH_TO_DATA_EN+'enwiki_20180920/en_names.csv.gz')

# load en pagelinks
df_en, df_red = functions.load_csvs_to_df(PATH_TO_DATA_EN+'enwiki_20180920/art_red/', ENWIKI_ART_FNMS)


# select non-translated articles
en_nontranslated = np.array(df_en_name[df_en_name['id_uk'].isnull()]['id'])
print('Nontranslated en acticles: %6d' % (len(en_nontranslated)))

# Encode en nontranslated articles which have at least 20 distinct incoming links
# input: ids of en_nontranslated articles, pagelinks_df with id,link_id columns
# output: two arrays which correspond by index, 1.ids, 2.encodings

en_nontranslated = df_en[df_en['link_id'].isin(ids_array)].groupby('link_id') \
        .agg({'id': lambda x: x.nunique()})
en_nontranslated = en_nontranslated.reset_index()
en_nontranslated.columns = ['id','n_incoming']
en_nontranslated = en_nontranslated[en_nontranslated['n_incoming']>=20]
en_nontranslated = np.array(en_nontranslated['id'])
en_nontranslated_ids = np.sort(en_nontranslated)
print('Nontranslated en acticles with at least 20 incoming links: %6d' % (len(en_nontranslated)))

en_nontranslated_encoding_df = df_en[df_en['link_id'].isin(en_nontranslated)]
en_nontranslated_encoding_df = en_nontranslated_encoding_df.sort_values(by = ['link_id','id'])
en_nontranslated_encoding_df = en_nontranslated_encoding_df.reset_index(drop = True)
indices = np.array(en_nontranslated_encoding_df.drop_duplicates(keep='first', subset=['link_id']).index)

en_nontranslated_encoding = []
pbar = progressbar.ProgressBar()
for i in pbar(range(0, len(indices))):
    if i == len(indices) - 1:
        this_encoding = set(en_nontranslated_encoding_df.iloc[indices[i]:]['id'])
    else: 
        this_encoding = set(en_nontranslated_encoding_df.iloc[indices[i]:indices[i+1]]['id'])
    en_nontranslated_encoding.append(this_encoding)

del en_nontranslated_encoding_df, en_nontranslated


# save encoding to file
np.save(PATH_TO_DATA+'en_nontranslated_encoding_draft.npy', arr=en_nontranslated_encoding)
np.save(PATH_TO_DATA+'en_nontranslated_ids_draft.npy', arr=en_nontranslated_ids)



# select non-translated acticles that have at least 20 distinct incoming links
en_nontranslated = df_en[df_en['link_id'].isin(en_nontranslated)].groupby('link_id') \
            .agg({'id': lambda x: x.nunique()})
en_nontranslated = en_nontranslated.reset_index()
en_nontranslated.columns = ['id','n_incoming']
en_nontranslated = en_nontranslated[en_nontranslated['n_incoming']>=20]
en_nontranslated = np.array(en_nontranslated['id'])
en_nontranslated_ids = np.sort(en_nontranslated)
print('Nontranslated en acticles with at least 20 incoming links: %6d' % (len(en_nontranslated)))


# encode each nontranslated article by its incoming links
en_nontranslated_encoding_df = df_en[df_en['link_id'].isin(en_nontranslated)]
en_nontranslated_encoding_df = en_nontranslated_encoding_df.sort_values(by = ['link_id','id'])
en_nontranslated_encoding_df = en_nontranslated_encoding_df.reset_index(drop = True)
indices = np.array(en_nontranslated_encoding_df.drop_duplicates(keep='first', subset=['link_id']).index)

en_nontranslated_encoding = []
pbar = progressbar.ProgressBar()
for i in pbar(range(0, len(indices))):
    if i == len(indices) - 1:
        this_encoding = set(en_nontranslated_encoding_df.iloc[indices[i]:]['id'])
    else: 
        this_encoding = set(en_nontranslated_encoding_df.iloc[indices[i]:indices[i+1]]['id'])
    en_nontranslated_encoding.append(this_encoding)
    
del en_nontranslated_encoding_df, en_nontranslated


# save encoding to file - rename for clean code!
np.save(PATH_TO_DATA+'en_nontranslated_encoding_draft.npy', arr=en_nontranslated_encoding)
np.save(PATH_TO_DATA+'en_nontranslated_ids_draft.npy', arr=en_nontranslated_ids)
