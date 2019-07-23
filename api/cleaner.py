from unidecode import unidecode
from re import sub


class dataCleaner():
    def __init__(self, data):
        self.data = data

    def decode_chars(self):
        self.data = {
            key: unidecode(value) for key, value in self.data.items()
        }

    def remove_special_char(self):
        self.data = {
            key: sub(r"[^a-z| ]", "", value.lower())
                for key, value in self.data.items()
        }

    def remove_stop_words(self):
        with open('../data/polish.stopwords.txt', 'r') as f:
            stop_words = f.read().split('\n')
        self.data = {
            key: " ".join([word.strip()
                    for word in value.split(' ')
                        if word.strip() not in stop_words and
                            len(word) > 1])
                for key, value in self.data.items()
        }

    def clean(self):
        self.decode_chars()
        self.remove_special_char()
        self.remove_stop_words()
        return self.data
