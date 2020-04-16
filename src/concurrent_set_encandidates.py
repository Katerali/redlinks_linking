#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import re
import numpy as np
import pickle
from multiprocessing import Pool

from src.utils import load_csvs_to_df_general, unpack, divide_number


def get_concurrent_set(page_id: int) -> (int, set):
    concurrent_set = set()
    for values in pagelinks_only_parents_dict.values():
        if page_id in values:
            concurrent_set = concurrent_set | set(values)
    return page_id, concurrent_set


def create_concurrent_set_uk(uk_pagelinks_filename: str,
                             rlsample_filename: str,
                             langlinks_filename: str,
                             output_filename) -> None:


PATH_TO_DATA_EN = '/media/andrii/earth/Katia/CS_MasterThesis/Red_links_Project_for_Wiki_01/data/enwiki/en_parsed/'
PATH_TO_DATA_UK = '/media/andrii/earth/Katia/CS_MasterThesis/Red_links_Project_for_Wiki_01/data/ukwiki/'

# Load candidate pairs
en_id_name = pd.read_csv(PATH_TO_DATA_EN + 'enwiki-20180920-id_name.csv', sep='^')

files = [f for f in os.listdir(PATH_TO_DATA_UK + 'candidates/') if re.match(r'[a-zA-Z]+_\d+.csv', f)]

candidate_pairs = load_csvs_to_df_general(PATH_TO_DATA_UK + 'candidates/', files)

# Load en pagelinks and prepare data for counting concurrent links of candidate pages
file_list = []
for file in os.listdir(PATH_TO_DATA_EN):
    if file.endswith("art.csv.gz"):
        file_path = os.path.join(PATH_TO_DATA_EN, file)
        file_list.append(file_path)

df_en_links_val_total = np.empty((0, 2), dtype=np.int)
for fname in file_list:
    fname_new = unpack(fname)
    df = pd.read_csv(fname_new, encoding='UTF-8', quotechar="\"", sep='^')
    if df['is_red_link'].dtype == 'bool':
        df_en_links = df[df['is_red_link'] == False][['id', 'link_id']]
    else:
        df_en_links = df[df['is_red_link'] == 'False'][['id', 'link_id']]

    df_en_links_val = df_en_links.values.astype(np.int)
    df_en_links_val_total = np.concatenate((df_en_links_val_total, df_en_links_val))
    os.remove(fname_new)

en_pagelinks = pd.DataFrame(df_en_links_val_total)
en_pagelinks.columns = ['parent_id', 'child_id']

# create {title: id} dict for candidates
candidates_list = candidate_pairs['candidate'].drop_duplicates().values.tolist()
en_candidates_df = en_id_name[en_id_name['title'].isin(candidates_list)]
candidates_dict = dict(zip(en_candidates_df['title'], en_candidates_df['en_wikipedia_id']))

pool = Pool()
candidates_id_list = pool.map(candidates_dict.get, candidates_list)
pool.close()
pool.join()

# RUN ONLY ONCE!! Creates a dict with filtered en pagelinks and saves to a file

# filter pagelinks keeping only with parent pages of candidates 
pagelinks_only_where_candidates = pd.merge(en_pagelinks, en_candidates_df, how='left', left_on=['child_id'],
                                           right_on=['en_wikipedia_id'])
parent_ids = pagelinks_only_where_candidates['parent_id'].drop_duplicates().values.tolist()
parent_ids_df = pd.DataFrame(parent_ids, columns=['parent_id'])
pagelinks_only_where_candidate_parents = pd.merge(en_pagelinks, parent_ids_df, how='left', left_on=['parent_id'],
                                                  right_on=['parent_id'])
pagelinks_parents = pagelinks_only_where_candidate_parents[['parent_id', 'child_id']]
pagelinks_parents = pagelinks_parents.drop_duplicates()

# convert en filtered pagelinks df to dictionary
pagelinks_only_parents_dict = {k: v['child_id'].tolist() for k, v in pagelinks_parents.groupby('parent_id')}

# RUN ONLY ONCE!! Retrieves the concurrent links for candidates and saves it to files
# results is pickle 101 file with concurrent links for English candidates

num_cand_list = divide_number(len(candidates_id_list), 100)

i = len(num_cand_list)
start_index = 0
num_items_proceed = num_cand_list[i - 1]

while i > 0:
    candidates_list_part = candidates_id_list[start_index:num_items_proceed]
    p = Pool()
    candidate_concurrent_set = p.map(get_concurrent_set, candidates_list_part)
    p.close()
    p.join()

    # save concurrent sets as a pickle file
    with open(PATH_TO_DATA_EN + 'concurrent_for_candidates/' + 'candidate_concurrent_set_' + str(i) + '.p', 'wb') as fp:
        pickle.dump(candidate_concurrent_set, fp, protocol=pickle.HIGHEST_PROTOCOL)

    i -= 1
    start_index = num_items_proceed
    num_items_proceed = num_items_proceed + num_cand_list[i - 1]
