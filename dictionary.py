import pandas as pd
"""Add words to the dictionary so that we can ignore them in the future"""

def AddWordsToDictionary(df, df_dict, df_temp):
    colname = 'polish'

    #Add the words to the dictionary
    dfdictlist = df_dict[colname].tolist()

    #Check to see if words from the temp dictionary are already in dictionary.  Keep track of words that already exist.
    remove_indices = []
    for index in range(len(df_temp)): 
        word = df_temp[colname].iloc[index]
        if word not in dfdictlist:
            dfdictlist.append(word)
        else:
            remove_indices.append(index)

    #We need to find the words in df that correspond to the indices to be removed from df
    for rindex in remove_indices:
        word = df_temp.iloc[rindex].polish
        rows = df.loc[df[colname] == word]
        if len(rows) == 1:
            index = rows.index.tolist()[0]
            df.drop(index, inplace=True)

    #Save the new dictionary
    df2 = pd.DataFrame({colname: dfdictlist})
    return df, df2