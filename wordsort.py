import numpy as np
import pandas as pd

def RemoveNewLineChar(lines: list) -> list:
    newlines = []
    for line in lines:
        newlines.append(line.split('\n')[0])
    return newlines

def SplitLines(lines: list, separator: str) -> list:
    newlines = []
    for line in lines:
        temp_lines = line.split(separator) #If a line consists of multiple sentences, split them up.
        for tline in temp_lines:
            if len(tline) > 0:
                newlines.append(tline)
    return newlines

def CreateWordFile(lines, template):
    #Get rid of new line character at the end of every line
    line_separators = ['.', '?', '!', ' - ']

    all_lines = RemoveNewLineChar(lines)
    for separator in line_separators:
        all_lines = SplitLines(all_lines, separator)

    all_words = []
    sentences = []
    for i, line in enumerate(all_lines):
        words = line.split(' ')
        all_words += words
        sentences += [line] * len(words)

    print("Total words = ", len(all_words))
    englishCol = [''] * len(all_words)
    template['polish'] = all_words
    template['polish_html'] = all_words
    template['sentence'] = sentences
    df_words = pd.DataFrame(template)
    #df_words = pd.DataFrame({'polish':all_words, 'english':englishCol, 'sentence':sentences})
    puncuation = ['.', ',', '?', '!', ':', ';']

    for index in range(len(df_words)):
        word = df_words['polish'].iloc[index]

    #for word in all_words:
        for p in puncuation:
            if p in word:
                word = word.split(p)[0]
                break 
        df_words.at[index, 'polish'] = word

    #Remove characters that match the following ASCII codes
    #bwords = []
    ascii_codes = [8222, 8221, 8220, 8223, 8230, 8219, 8218, 8217, 8216, 160, 34, 40, 41]
    for index in range(len(df_words)):
        word = df_words['polish'].iloc[index]
    #for word in fixed_words:
        s = ""
        for c in word:
            if ord(c) not in ascii_codes:
                s += c
        df_words.at[index, 'polish'] = s
        df_words.at[index, 'polish_html'] = s
        #bwords.append(s)

    #Make all words lowercase
    for index in range(len(df_words)):
        word = df_words['polish'].iloc[index]
    #for word in bwords:
        #lower_words.append(word.lower())
        df_words.at[index, 'polish'] = word.lower()
        df_words.at[index, 'polish_html'] = word.lower()

    #Remove words that are numbers
    remove_indices = []
    for index in range(len(df_words)):
        word = df_words['polish'].iloc[index]
        if word.isdigit():
            remove_indices.append(index)

    #print("Remove these indices: ", remove_indices)
    df_words.drop(remove_indices, inplace=True)
    df_words.reset_index(inplace=True, drop=True)

    #Remove 1 letter words
    remove_indices = []
    for index in range(len(df_words)):
        word = df_words['polish'].iloc[index]
        if len(word) == 1:
            remove_indices.append(index)

    #print("Remove these indices: ", remove_indices)
    df_words.drop(remove_indices, inplace=True)
    df_words.reset_index(inplace=True, drop=True)
    
    # dropping ALL duplicate values
    df_words.drop_duplicates(subset="polish", keep="first", inplace=True)
    df_words.reset_index(inplace=True, drop=True)

    #Remove entries that appear in the dictionary
    dicname = "dictionary.csv"
    try:
        df_dic = pd.read_csv("csv/" + dicname)
    except:
        print("Dictionary does not exist")
    else:
        remove_indices = []
        diclist = df_dic['polish'].tolist()
        for index in range(len(df_words)):
            word = df_words['polish'].iloc[index]
            if word in diclist:
                remove_indices.append(index)

        print("Remove these indices: ", remove_indices)
        print("Number of words already in dictionary = ", len(remove_indices))
        df_words.drop(remove_indices, inplace=True)
        df_words.reset_index(inplace=True, drop=True)
  
    return df_words  

