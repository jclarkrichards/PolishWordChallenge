import pandas as pd
"""Add words to the dictionary so that we can ignore them in the future"""

def AddWordsToTempDictionary(df, df_temp):
    colname = 'polish'

    dfdictlist = df_temp[colname].tolist()
    print("Before there are ", len(dfdictlist), " rows")

    for index in range(len(df)):
        word = df[colname].iloc[index]
        if word not in dfdictlist:
            dfdictlist.append(word)

    print("After there are ", len(dfdictlist), " rows")

    #Save the new dictionary
    df2 = pd.DataFrame({colname: dfdictlist})
    return df2