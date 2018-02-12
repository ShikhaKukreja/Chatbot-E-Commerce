import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

class TockenizeData:

    @staticmethod
    def getTockenizedDataWithStem(statement):
        tokens = nltk.word_tokenize(statement)

        filtered_words = [word for word in tokens if word not in stopwords.words('english')]

        f = []
        LS = LancasterStemmer()
        for ff in filtered_words:
            f.append(LS.stem(ff))
        return f

    @staticmethod
    def getTockenizedData(statement):
        tokens = nltk.word_tokenize(statement)
        filtered_words = [word for word in tokens if word not in stopwords.words('english')]
        return filtered_words
