import pandas as pd

csvname = 'ep194.csv'
df = pd.read_csv(csvname)
df_shuffled = df.sample(frac=1)
df_shuffled = df_shuffled[['polish', 'english', 'check']]
df_shuffled.reset_index(inplace=True, drop=True)
df_shuffled.to_csv(csvname)