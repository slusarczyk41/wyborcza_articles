from unidecode import unidecode
from re import sub


class dataCleaner():
    def __init__(self, columns):
        self.columns = columns

    def decode_chars(self):
        return {
            key: unidecode(value) for key, value in self.data.items()
                if key in self.columns
        }

    def remove_special_char(self):
        return {
            key: sub(r"[^a-z| ]", "", value.lower())
                for key, value in self.data.items()
                    if key in self.columns
        }

    def remove_stop_words(self):
        with open('../data/polish.stopwords.txt', 'r') as f:
            stop_words = f.read().split('\n')
        return {
            key: " ".join([word.strip()
                    for word in value.split(' ')
                        if word.strip() not in stop_words and
                            len(word) > 1])
                for key, value in self.data.items()
                    if key in self.columns
        }

    def clean(self, incomingData):
        self.data = incomingData
        self.decode_chars()
        self.remove_special_char()
        self.remove_stop_words()
        returnDict = {}
        for key, value in incomingData.items():
            if key not in self.columns:
                returnDict[key] = value
            else:
                returnDict[key] = self.data[key]
        return returnDict
