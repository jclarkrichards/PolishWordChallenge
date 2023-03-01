from googletrans import Translator
import pandas as pd

def AddEnglishTranslations(df):
    translator = Translator()
    for i in list(range(len(df))):
        translation = translator.translate(df.iloc[i].polish, src="pl", dest="en")
        result = translation.text
        df.loc[df.iloc[i].name, "english"] = result.lower().strip()
        print(df.iloc[i].polish, "  ", result)

        translation = translator.translate(df.iloc[i].english, src="en", dest="pl")
        result2 = translation.text
        df.loc[df.iloc[i].name, "check"] = result2.lower().strip()
        #print(df.iloc[i].polish, "  ", result2)

    return df
    