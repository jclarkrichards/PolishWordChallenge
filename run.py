import argparse
import pandas as pd
from wordsort import CreateWordFile
from dictionary_temp import AddWordsToTempDictionary
from dictionary import AddWordsToDictionary
from translate import AddEnglishTranslations

parser = argparse.ArgumentParser(description="description of sorts")
parser.add_argument("-f", "--file", type=str, help="The name of the file to use.  Must include extension.  filename.txt for example")
parser.add_argument("-s", "--script", type=str, help="The function to use:  'Create', 'Temp', 'Dict', 'Translate', 'HTML', 'Shuffle', 'English', 'Polish', 'Update'",
                    choices=['Create', 'Temp', 'Dict', 'Translate', 'HTML', 'Shuffle', 'Finish', 'English', 'Polish', 'Update'], default='Create')



class FlashCards(object):
    def __init__(self, filename):
        self.columns = ['polish', 'check', 'english', 'sentence', 'polish_html', 'english_html', 'sentence_html']
        self.template = {'polish':"", 'check':"", 'english':"", 'sentence':"", 'polish_html':"", 'english_html':"", 'sentence_html':""}
        self.filename, self.ext = filename.split('.')
        self.filename = self.filename.strip()
        self.ext = self.ext.strip()
        self.df = None
        print(filename, self.filename, self.ext)
        #test = pd.read_csv("csv/"+filename)
        if self.ext == "txt":
            self.rawlines = self.OpenTranscriptFile()
        elif self.ext == "csv":
            self.df = self.OpenCSVFile(self.filename)
        

    def OpenTranscriptFile(self):
        '''These files have a .txt extension and are the raw text'''
        print("Open Txt")
        with open("transcripts/" + self.filename+'.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    def OpenCSVFile(self, filename):
        print("Open CSV ", filename)
        s = "csv/"+filename+".csv"
        print("File to open: ", s)
        #df = pd.read_csv(s)
        try:
            df = pd.read_csv(s)
        except:
            print(s, "does not exist, so create")
            df = pd.DataFrame(columns=self.columns)
        return df

    def SaveFile(self, df, filename="replaceMe", sortCol="polish"):
        '''All files get saved in the csv directory and have .csv extension'''
        print("Save CSV")
        df.sort_values(sortCol, inplace=True)
        df.reset_index(inplace=True, drop=True)
        #print(df.columns)
        columns = ['polish', 'check', 'english', 'sentence', 'polish_html', 'english_html', 'sentence_html']
        if sortCol == 'english':
            columns = ['english', 'polish', 'check', 'sentence', 'polish_html', 'english_html', 'sentence_html']

        df = df[[k for k in columns if k in df.columns]]
        df.to_csv("csv/" + filename+".csv")  

    def CreateEmptyDataFrame(self):
        return pd.DataFrame(columns=self.columns)

    def GetLinesFromFile(self):
        pass

    def CreateInitialFile(self):
        print("CeateInitialFile")
        df = CreateWordFile(self.rawlines, self.template)
        self.SaveFile(df, self.filename)
        print(self.filename)
        self.df = self.OpenCSVFile(self.filename)
        self.TempDictionary()

    def TempDictionary(self):
        print("TempDictionary")
        df_temp = self.OpenCSVFile("dictionary_temp")
        print(self.df.head())
        print(df_temp.head())
        df = AddWordsToTempDictionary(self.df, df_temp)
        self.SaveFile(df, "dictionary_temp")


    def UpdateDictionary(self):
        print("UpdateDictionary")
        df_dict = self.OpenCSVFile("dictionary")
        df_temp = self.OpenCSVFile("dictionary_temp")
        #print(self.df.head())
        #print(df_temp.head())
        df, df_dict = AddWordsToDictionary(self.df, df_dict, df_temp)
        self.SaveFile(df_dict, "dictionary")
        self.SaveFile(df, self.filename)

    def Translate(self):
        df = AddEnglishTranslations(self.df)
        self.SaveFile(df, self.filename)

    def Shuffle(self):
        #df = pd.read_csv(csvname)
        df_shuffled = self.df.sample(frac=1)
        self.SaveFile(df_shuffled, self.filename)
        #df_shuffled = df_shuffled[['polish', 'english', 'check']]
        #df_shuffled.reset_index(inplace=True, drop=True)
        #df_shuffled.to_csv(csvname)

    def HTMLSentence(self):
        spantag = "<span style='color:rgb(0, 180, 250)'>"
        spanendtag = "</span>"
        #print(self.df.head())
        for index in range(len(self.df)):
            sentence = self.df['sentence'].iloc[index]
            words = sentence.split(" ")
            sentence_html = "<p><i><h6>"
            for w in words:     
                sentence_html += w + " "
            sentence_html += "</h6></i></p>"
            self.df.loc[self.df.iloc[index].name, "sentence_html"] = sentence_html

        #self.SaveFile(self.df, self.filename)

    def HTMLEnglish(self):
        for index in range(len(self.df)):
            eword = self.df['english'].iloc[index]
            eword_html = "<h3>" + eword + "</h3>"
            self.df.loc[self.df.iloc[index].name, "english_html"] = eword_html

    def HTMLPolish(self):
        for index in range(len(self.df)):
            pword = self.df['polish'].iloc[index]
            pword_html = "<h4 style='color:rgb(0, 180, 250)'>" + pword + "</h4>"
            self.df.loc[self.df.iloc[index].name, "polish_html"] = pword_html

    def CombinePolishSentence(self):
        for index in range(len(self.df)):
            polishHTML = self.df['polish_html'].iloc[index]
            sentenceHTML = self.df['sentence_html'].iloc[index]
            self.df.loc[self.df.iloc[index].name, "polish_html"] = polishHTML + "    " + sentenceHTML


    def AddHTMLEntries(self):
        spantag = "<span style='color:rgb(0, 180, 250)'>"
        spanendtag = "</span>"
        print(self.df.head())
        for index in range(len(self.df)):
            pword = self.df['polish_html'].iloc[index]
            sentence = self.df['sentence'].iloc[index]
            words = sentence.split(" ")
            sentence_html = "<p><i><h6>"
            for w in words:
                print(pword, w)
                if pword.strip() in w.lower().strip():
                    sentence_html += spantag+w+spanendtag + " "
                else:
                    sentence_html += w + " "

            sentence_html += "</h6></i></p>"
            self.df.loc[self.df.iloc[index].name, "sentence_html"] = sentence_html

        self.SaveFile(self.df, self.filename)

    def Finish(self):
        '''Need to combine the polish_html and sentence_html into just the polish_html'''
        for index in range(len(self.df)):
            pword = self.df['polish'].iloc[index]
            sentence = self.df['sentence_html'].iloc[index]
            eword = self.df['english'].iloc[index]

            pword_html = "<h4 style='color:rgb(0, 180, 250)'>" + pword + "</h4>"
            eword_html = "<h3>" + eword + "</h3>"
            self.df.loc[self.df.iloc[index].name, "english_html"] = eword_html
            self.df.loc[self.df.iloc[index].name, "polish_html"] = pword_html + "    " + sentence
        self.SaveFile(self.df, self.filename)

    def SortEnglish(self):
        self.SaveFile(self.df, self.filename, 'english')

    def SortPolish(self):
        self.SaveFile(self.df, self.filename)

    def Update(self):
        '''Take the polish, english, and sentence columns and turn them into html'''
        self.HTMLSentence()
        self.HTMLEnglish()
        self.HTMLPolish()
        self.CombinePolishSentence()
        self.SaveFile(self.df, self.filename)







if __name__ == "__main__":
    args = parser.parse_args()
    print(args.file)
    print(args.script)
    app = FlashCards(args.file)

    if args.script == "Create":
        app.CreateInitialFile()
    elif args.script == "Temp":
        app.TempDictionary()
    elif args.script == "Dict":
        app.UpdateDictionary()
    elif args.script == "Translate":
        app.Translate()
    elif args.script == "HTML":
        app.AddHTMLEntries()
    elif args.script == "Shuffle":
        app.Shuffle()
    elif args.script == "Finish":
        app.Finish()
    elif args.script == "English":
        app.SortEnglish()
    elif args.script == "Polish":
        app.SortPolish()
    elif args.script == "Update":
        app.Update()
