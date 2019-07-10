from unidecode import unidecode
from re import sub


class dataCleaner():
    def __init__(self):
        return None
    
    def feed_with_data(self, data):
        self.data = data

    def decode_chars(self):
        return {
            key: unidecode(value) for key, value in self.data.items()
        }

    def remove_special_char(self):
        return {
            key: sub(r"[^a-z| ]", "", value.lower())
                for key, value in self.data.items()
        }

    def remove_stop_words(self):
        with open('data/polish.stopwords.txt', 'r') as f:
            stop_words = f.read().split('\n')
        return {
            key: " ".join([word.strip()
                    for word in value.split(' ')
                        if word.strip() not in stop_words])
                for key, value in self.data.items()
        }

    def clean(self):
        self.decode_chars()
        self.remove_special_char()
        self.remove_stop_words()
        return self.data
