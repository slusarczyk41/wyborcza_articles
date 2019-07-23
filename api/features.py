from app import cache
from collections import Counter
import numpy as np
from datetime import datetime as dt
from json import load


class featureMaker():
    def __init__(self, data, word2vec_path):
        self.data = data
        self.word2vec_path = word2vec_path
        self.columns = ['title', 'media_desc', 'highlight', 'content']
        self.months = {
            'stycznia': 1,
            'lutego': 2,
            'marca': 3,
            'kwietnia': 4,
            'maja': 5,
            'czerwca': 6,
            'lipca': 7,
            'sierpnia': 8,
            'września': 9,
            'października': 10,
            'listopada': 11,
            'grudnia': 12
        }

    cache.cached(timeout=60)
    def read_idf(self):
        with open('../data/idf') as f:
            idf = f.read().split('\n')
        return {pair.split(' ')[0]: int(pair.split(' ')[1]) for pair in idf if pair != ''}

    cache.cached(timeout=60)
    def read_word2vec(self):
        with open(self.word2vec_path) as f:
            lines = f.read().split('\n')
        return {
            x.split(' ')[0]: [float(x) for x in x.split(' ')[1:]] for x in lines
        }

    cache.cached(timeout=60)
    def read_dictionaries(self):
        dictionaries = {}
        for column in ['author', 'division', 'media']:
            with open('../labeling/'+column+"_dict") as f:
                dictionaries[column] = load(f)
        self.dicts = dictionaries

    def calculate_tf(self):
        bag_of_all_words = " ".join([value for key, value in self.data.items()
                                                if key in self.columns])
        tf = dict(Counter([word for word in bag_of_all_words.split(' ')]))
        return tf

    def calculate_tf_idf(self):
        tf = self.calculate_tf()
        idf = self.read_idf()
        return [tf[word]/idf if word in tf.keys() else 0
                    for word, idf in idf.items()]

    def calculate_vectors(self):
        word2vec = self.read_word2vec()
        word2vec_vocabulary = word2vec.keys()

        vectors_container = []
        for column in self.columns:
            vector = np.zeros(300, dtype = "float64")
            n_words = 0
            for word in self.data[column].split(' '):
                if word in word2vec_vocabulary:
                    vector = np.add(vector, word2vec[word])
                    n_words += 1
            if n_words:
                vector = np.divide(vector, n_words)
            vectors_container.append(vector.tolist())

        return [x for x in [i for i in vectors_container] for x in x]

    def process_date(self):
        date = self.data['date']
        year = date.split('|')[0].split(' ')[2].strip()
        month = str(self.months[date.split('|')[0].split(' ')[1].strip()])
        day = date.split('|')[0].split(' ')[0].strip()

        try:
            hour = date.split('|')[1].strip()
        except:
            return None
        return dt.strptime(" ".join([year, month, day, hour]), "%Y %m %d %H:%M")

    def get_dummy_dates(self):
        return_list = [0 for i in range(7+24)]
        processed_date = self.process_date()
        return_list[processed_date.weekday()] = 1
        return_list[processed_date.hour+6] = 1
        return return_list

    def get_dummies_from(self, type):
        return_list = [0 for x in range(len(self.dicts[type]))]
        if self.data[type] in self.dicts[type].keys():
            i = self.dicts[type][self.data[type]]
            return_list[i] = 1
        return return_list

    def process(self):
        tf_idf = self.calculate_tf_idf()
        # one list with length same as idf

        vectors = self.calculate_vectors()
        # list of vectors for each content type

        dummy_dates = self.get_dummy_dates()
        # dates dummies

        self.read_dictionaries()

        author_dummy = self.get_dummies_from('author')
        # author dummies

        division_dummy = self.get_dummies_from('division')
        # division dummies

        media_type_dummy = self.get_dummies_from('media')
        # media type dummies
        print(len(dummy_dates + author_dummy + media_type_dummy + division_dummy +\
                vectors + tf_idf))
        return dummy_dates + author_dummy + media_type_dummy + division_dummy +\
                vectors + tf_idf
