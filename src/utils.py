import os
import re
import gzip
import time
import pandas as pd
import numpy as np
import transliterate
from transliterate import translit, get_available_language_codes



# wrap your csv importer in a function that can be mapped
def read_csv(filename):
    'converts a filename to a pandas dataframe'
    print(filename)
    return pd.read_csv(filename, encoding='UTF-8', quotechar="\"")

def unpack(file_name):
    file_name_new = file_name.replace(".gz","")
    with gzip.open(file_name, 'rb') as f_in, open(file_name_new, 'wb') as f_out:
        f_out.writelines(f_in)
    return file_name_new


def pack_and_remove(file_name):
    file_name_new = file_name+'.gz'
    with open(file_name, 'rb') as f_in, gzip.open(file_name_new, 'wb') as f_out:
        f_out.writelines(f_in)
    os.remove(file_name)
    return file_name_new


def get_scripts(x):
    x_set = ad.detect_alphabet(str(x))
    x_list = list(x_set)
    x_string = ' '.join(x_list)
    return x_string


def extract_list(s):
    return [x.split(',')[1].strip("', ,\"") for x in s[2:-2].split('), (')]

def divide_number(total, by):
    part = total//by
    list_numbers = [part] * by
    if total - (part*by) > 0:
        list_numbers.append(total%by)
    return list_numbers

def get_id_from_nested_dict(dict_):
    try:
        key1 = list(dict_)[1]
        query_dict = dict_.get(key1)
        key2 = list(query_dict)[0]
        pages_dict = query_dict.get(key2)
        key3 = list(pages_dict)[0]
        more_dict = pages_dict.get(key3)
        key4 = list(more_dict)[3]
        pageprops_dict = more_dict.get(key4)
        id_ = pageprops_dict.get('wikibase_item')
    except:
        id_ = None
    return id_


def get_instance_id_from_nested_dict(dict_):
    try:
        key1 = list(dict_)[0]
        entities_dict = dict_.get(key1)
        key2 = list(entities_dict)[0]
        item_dict = entities_dict.get(key2)
        claims_dict = item_dict.get('claims')
        instance_dict = claims_dict.get('P31')
        id_dict = instance_dict[0]
        mainsnak_dict = id_dict.get('mainsnak')
        datavalue_dict = mainsnak_dict.get('datavalue')
        value_dict = datavalue_dict.get('value')
        instance_id = value_dict.get('id')
    except:
        instance_id = None
    return instance_id


def get_instance_name_from_nested_dict(dict_):
    try:
        entities_dict = dict_.get('entities')
        key = list(entities_dict)[0]
        id_key = entities_dict.get(key)
        labels_dict = id_key.get('labels')
        en_dict = labels_dict.get('en')
        final_value = en_dict.get('value')
    except:
        final_value = None
    return final_value


def read_csv(filename):
    'converts a filename to a pandas dataframe'
    print(filename)
    return pd.read_csv(filename, encoding='UTF-8', quotechar="\"")


def extract_score(s):
    return [float(x.split(',')[0].strip("', ,\"")) for x in s[2:-2].split('), (')]


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



def calculate_norm_levenstein_df(row):
    red_link = str(row['red_link_name'])
    candidate = str(row['candidate'])
    abs_dist = levenshteinDistance(translit(red_link, 'uk', reversed=True), candidate)
    norm_dist = abs_dist/max(len(red_link), len(candidate))
    norm_dist = round(norm_dist, 3)
    return norm_dist




def f1_score(evaluation_results, with_print=True):
    res = evaluation_results.value_counts()
    try:
        tp = res['TP']
    except:
        tp = 0
    
    try:
        tn = res['TN']
    except:
        tn = 0

    try:
        fp = res['FP']
    except:
        fp = 0

    try:
        fn = res['FN']
    except:
        fn = 0
    
    precision = 0 if tp + fp == 0 else tp/(tp + fp)
    recall = 0 if tp + fn == 0 else tp/(tp + fn)
    

    f1_score = 0 if precision + recall == 0 else 2 * precision * recall/(precision + recall)
    if with_print:
        print('FP =', round(fp, 3))
        print('TN =', round(tn, 3))
        print('TP =', round(tp, 3))
        print('FN =', round(fn, 3))
        print('precision =', round(precision, 3))
        print('recall =', round(recall, 3))
        print('f1_score =', round(f1_score, 3))
    
    return precision, recall, f1_score



def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


def jaccard(a, b):
    c = a.intersection(b)
    return len(c) / (len(a) + len(b) - len(c))


def decode_df_from_to(dataframe, from_, to_):
    f = lambda x: x.encode(from_)
    dataframe_encoded = dataframe.applymap(f)
    
    f_decode = lambda x: x.decode(to_)
    dataframe_decoded = dataframe_encoded.applymap(f_decode)
    
    return dataframe_decoded



# loading all articles to dataframe function
def load_csvs_to_df_spec(path, list_of_fnms):
    start_time = time.time()
    df_blue = pd.DataFrame()
    df_red = pd.DataFrame()
    n_files = len(list_of_fnms)
    print(n_files)
    
    for index in range(1):
        print(str(index+1) + '/' + str(n_files))
        fn = list_of_fnms[index]
        fn = path+fn
        print(fn)
        #fn_new = unpack(fn)/instead:
        fn_new = fn
        
        df_articles = pd.read_csv(fn_new, encoding='UTF-8', quotechar="\"")  
        df_articles_blue = df_articles[df_articles['is_red_link']==False]
        df_blue = pd.concat((df_blue, df_articles_blue[['id','link_id']]))
        df_articles_red = df_articles[df_articles['is_red_link']]
        df_red = pd.concat((df_red, df_articles_red[['id','link_val']]))
        
        #os.remove(fn_new)
    
    print('Total time: %.1f minutes' % ((time.time() - start_time)/60))
    return df_blue, df_red



def load_csvs_to_df_general(path, list_of_fnms):
    start_time = time.time()
    df = pd.DataFrame()
    n_files = len(list_of_fnms)
    #print(n_files)
    
    for index in range(n_files):
        #print(str(index+1) + '/' + str(n_files))
        fn = list_of_fnms[index]
        fn_new = path+fn
        #print(fn_new)
        
        df_articles = pd.read_csv(fn_new, encoding='UTF-8',sep='^')  
        df = pd.concat((df, df_articles))

    
    #print('Total time: %.1f minutes' % ((time.time() - start_time)/60))
    return df




# add ids for red links
def ids_red_links(blue_ids_series, red_link_all_series):
    max_id = np.max(blue_ids_series)
    red_links = red_link_all_series.unique()
    red_links_ids = pd.DataFrame({'title': red_links, 
                              'id': np.arange(max_id+1, len(red_links)+max_id+1)})
    return red_links_ids



def train_test_split(path, sample_df):
    msk = np.random.rand(len(sample_df)) < 0.8
    train = sample_df[msk]
    test = sample_df[~msk]

    print('train length =', len(train))
    print('test length =', len(test))
    
    train.to_csv(path+'train_set.csv', index=False, sep='^')
    test.to_csv(path+'test_set.csv', index=False, sep='^')


def train_test_split_update(path_pairs, path_sample, path_out):
    
    # load data
    candidate_pairs = pd.read_pickle(path_pairs)
    sample = pd.read_pickle(path_sample)

    sample_red_links_names = sample.red_link_name.unique()
    
    msk = np.random.rand(len(sample_red_links_names)) < 0.8
    
    sample_red_links_names_train = sample_red_links_names[msk]
    sample_red_links_names_test = sample_red_links_names[~msk]
    
    train = candidate_pairs[candidate_pairs['red_link_name'].isin(sample_red_links_names_train)]
    test = candidate_pairs[candidate_pairs['red_link_name'].isin(sample_red_links_names_test)]
    
    print('train length =', len(train))
    print('test length =', len(test))
    
    train.to_csv(path_out + 'train_set.csv', index=False, sep='^')
    test.to_csv(path_out + 'test_set.csv', index=False, sep='^')


def divide_number(total, by):
    part = total//by
    list_numbers = [part] * by
    if total - (part*by) > 0:
        list_numbers.append(total%by)
    return list_numbers


def files_to_df(path_folder):
    files = os.listdir(path_folder)
    scores_per_folder = []
    for file in files:
        with open(path_folder+file, 'rb') as fp:
            concurrent_scores = pickle.load(fp)
        scores_per_folder += concurrent_scores
    df = pd.DataFrame(scores_per_folder)
    df.columns = ['pair_id', 'concur_score']
    df = df.dropna()
    return df

def jaccard_similarity_on_concurrent_links(triple):
    cand_id = triple[0]
    red_link = triple[1]
    pair_id = triple[2]
    

    en_set = candidate_concurrent_sets_dict.get(cand_id)
    uk_set = uk_concurrent_links_dict.get(red_link)

    if en_set is None:
        jaccard_score = None
    
    elif uk_set is None:
        jaccard_score = None
    else:
        jaccard_score = utils.jaccard(uk_set, en_set)
        jaccard_score = round(jaccard_score, 5)
        
    del en_set
    del uk_set
        
        
    return (pair_id, jaccard_score)

