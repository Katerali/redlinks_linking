# this file queries Uk translations for En red links from BabelNet for a sample (up to 1000 part of BableNet sample as a key limit allows)
# input file must contain a 'red_link_name' column with a red link sample.


# to get translations from a Wikidata base of BabelNet, in a query change 'source=WIKIDATA'
# to get translations for other languages, in a query change 'searchLang' and targetLang'



from collections import defaultdict
import requests
import pandas as pd

# insert an access key
myKey = '531f74dc-1ec7-4390-b5db-65f6f1b75aaa'

PATH_TO_DATA = '/media/andrii/earth/Katia/CS_MasterThesis/data/ukwiki/uk_red_links/'
filename = "df_sample_red_links_uk_sample_tmp.csv"

PATH_OUT = '/media/andrii/earth/Katia/CS_MasterThesis/data/ukwiki/uk_red_links/'
# rename a file for a current sample!!
filename_out = 'BabelNet_wiki.csv'

# open 
sample = pd.read_csv(PATH_TO_DATA+filename, encoding='UTF-8')

list_of_red_links = sample['red_link_name'].tolist()

# may help
#list_of_red_links = [s.strip('\u200e') for s in list_of_red_links]

total_list_of_results = []
#f1=open('./requests_results_wiki.txt', 'w+')
for link in list_of_red_links:
    url = "https://babelnet.io/v5/getSenses?lemma=" + link + "&searchLang=UK&targetLang=EN&source=WIKI&key="+myKey
    response = requests.get(url)
#    f1.write(response.text + "\n\n")
    json_response = response.json()
    if json_response == []:
        total_list_of_results.append(defaultdict(list))
    else:
        dd = defaultdict(list)
        row = []
        for i in json_response:
            found = {}
            lemma = i['properties']['fullLemma']
            language = i['properties']['language']
            found.update( {language: lemma} )
            row.append(found)
        for d in row:
            for key, value in d.items():
                dd[key].append(value)
        for lang in dd:
            s = ', '.join(dd[lang])
            dd[lang] = [s]
        total_list_of_results.append(dd)
#f1.close()


part_wiki = pd.DataFrame(total_list_of_results)


part_wiki.to_csv(PATH_OUT+filename_out, index=False)

