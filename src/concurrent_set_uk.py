
import pandas as pd
import gzip
import os
import pickle


def create_concurrent_set_uk(uk_pagelinks_filename: str,
                             rlsample_filename: str,
                             langlinks_filename: str,
                             output_filename) -> None:
    """
    This function creates a set of unique concurrent links for Ukrainian red links sample.
    Concurrent links are links which occur in the same Wikipedia articles as red links.
    The function uses beforehand prepared dataframes of links between pages in Ukrainian
    and English Wikipedia.

    # Parameters

    uk_pagelinks_filename : str
        Name of a file. Contents a dataframe with all links between all pages in Ukrainian Wikipedia.
    rlsample_filename : str
        Name of a file. Contents a dataframe with a sample of Ukrainian red links.
    langlinks_filename: str
        Name of a file. Contents a dataframe with page ids correspondences between English and Ukrainian Wikipedia editions.
    output_filename: str
        Name of a final pickle file which contents a set of unique concurrent links for Ukrainian red links sample.

    # Returns
        None
    """

    df_uk_pagelinks = pd.read_csv(uk_pagelinks_filename)
    rlsample = pd.read_csv(rlsample_filename, sep='^')
    langlinks_df = pd.read_csv(langlinks_filename, sep='^')

    df_rl_with_all_parents = pd.merge(df_uk_pagelinks, rlsample, how='inner', left_on='link_val', right_on='red_link_name')
    df_rl_with_all_parents = df_rl_with_all_parents[['id', 'link_id', 'link_val']]

    rl_with_concurrent = pd.merge(df_rl_with_all_parents, df_uk_pagelinks, how='left', left_on='id', right_on='id')
    rl_with_concurrent = rl_with_concurrent[['id', 'link_val_x', 'link_id_y', 'link_val_y']]
    rl_with_concurrent.columns = ['parent_id', 'red_link_name', 'concurrent_id', 'concurrent_name']
    rl_with_concurrent = rl_with_concurrent.drop_duplicates()

    rl_with_concurrent_enwiki = pd.merge(rl_with_concurrent, langlinks_df, how='left', left_on='concurrent_id', right_on='ll_from')
    rl_with_concurrent_enwiki = rl_with_concurrent_enwiki[['red_link_name', 'id']]
    rl_with_concurrent_enwiki.columns = ['red_link_name', 'enwiki_id']
    rl_with_concurrent_enwiki_clean = rl_with_concurrent_enwiki[pd.notna(rl_with_concurrent_enwiki['enwiki_id'])]

    uk_concurrent_links_dict = {k: set(v['enwiki_id']) for k,v in rl_with_concurrent_enwiki_clean.groupby('red_link_name')}
    
    with open(output_filename, 'wb') as fp:
        pickle.dump(uk_concurrent_links_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)






