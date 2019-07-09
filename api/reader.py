from endpoint import cache



cache.cached(timeout=60)
def read_idf(self):
    with open('../data/idf') as f:
        idf = f.read().split('\n')
    return idf
