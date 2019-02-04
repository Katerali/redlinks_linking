from alphabet_detector import AlphabetDetector
ad = AlphabetDetector()

# to get the names of scripts in a dataframe. Results written below.
#def get_scripts(x):
#    x_set = ad.detect_alphabet(str(x))
#    x_list = list(x_set)
#    x_string = ' '.join(x_list)
#    return x_string




cyrillic_scripts = ['CYRILLIC', 'CYRILLIC MODIFIER', 'MASCULINE CYRILLIC']

latin_scripts = ['LATIN', 'LATIN MASCULINE', 'LATIN MICRO', 'LATIN MODIFIER', 'LATIN FEMININE']

greek_scripts = ['GREEK']

cjk_scripts = ['CJK',
               'HIRAGANA CJK',
               'KATAKANA',
               'KATAKANA-HIRAGANA HIRAGANA',
               'KATAKANA-HIRAGANA KATAKANA',
               'KATAKANA CJK',
               'HIRAGANA',
               'KATAKANA-HIRAGANA KATAKANA HIRAGANA CJK',
               'HANGUL',
               'KATAKANA-HIRAGANA KATAKANA CJK',
               'IDEOGRAPHIC CJK',
               'KATAKANA-HIRAGANA KATAKANA HIRAGANA']

arabic_scripts = ['ARABIC']

armenian_scripts = ['ARMENIAN']

georgian_scripts = ['GEORGIAN']

mixed_scripts = ['mixed',
                 'LATIN CYRILLIC',
                 'LATIN MASCULINE CYRILLIC',
                 'MICRO CYRILLIC',
                 'LATIN CYRILLIC MODIFIER',
                 'GREEK CYRILLIC',
                 'LATIN GREEK',
                 'CYRILLIC CJK',
                 'LATIN GREEK CYRILLIC',
                 'LATIN CYRILLIC CJK',
                 'LATIN CYRILLIC HANGUL',
                 'LATIN KATAKANA HIRAGANA',
                 'LATIN KATAKANA-HIRAGANA KATAKANA',
                 'LATIN CJK',
                 'KATAKANA-HIRAGANA LATIN KATAKANA',
                 'CYRILLIC HIRAGANA CJK']

number_scripts = ['number', '']

symbol_scripts = ['symbol', 'HALFWIDTH']






def calculate_script_stats(script_list, df, column_name):
    len_s = 0
    for s in script_list:
        len_s += len(df[df[column_name]==s])
        script_perc = len_s/len(df)
    print(script_list[0], len_s)
    print('script_perc', script_list[0], script_perc)








