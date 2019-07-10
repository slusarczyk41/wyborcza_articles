from app import cache
from collections import Counter
import numpy as np


class featureMaker():
    def __init__(self, data, columns, word2vec_path):
        self.columns = columns
        self.data = data
        self.word2vec_path = word2vec_path

    cache.cached(timeout=60)
    def read_idf(self):
        with open('../data/idf') as f:
            idf = f.read().split('\n')
        return {pair.split(' ')[0]: int(pair.split(' ')[1]) for pair in idf if pair != ''}

    # cache.cached(timeout=60)
    def read_word2vec(self):
        with open(self.word2vec_path) as f:
            lines = f.read().split('\n')
        return {
            x.split(' ')[0]: [float(x) for x in split(' ')[1:]] for x in lines
        }

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
            vectors_container.append(vector)

        return vectors_container

    def process(self):
        tf_idf = self.calculate_tf_idf()
        # vectors = self.calculate_vectors()

        return tf_idf
