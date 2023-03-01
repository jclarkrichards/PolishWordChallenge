import pandas as pd

csvname = 'words.csv'
df = pd.read_csv(csvname)

colnames = ['english', 'polish']
dfnew = pd.DataFrame(columns=colnames)

for i in list(range(len(df))):
    if df.iloc[i].polish == df.iloc[i].check:
        #print("add to sample")
        #row = pd.Series([df.iloc[i].english, df.iloc[i].polish], index=df.columns)
        dtemp = {'english':df.iloc[i].english, 'polish':df.iloc[i].polish}
        dfnew = dfnew.append(dtemp, ignore_index=True)
        #dfnew = dfnew.append(row, ignore_index=True)


dfnew.reset_index(inplace=True, drop=True)
dfnew.to_csv("sample.csv")