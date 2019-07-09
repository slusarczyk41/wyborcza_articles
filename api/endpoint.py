from app import app

from flask import jsonify
from cleaner import dataCleaner
from features import featureMaker
# from models import modelsHandler
# https://stackoverflow.com/questions/53042856/how-can-i-pass-a-dictionary-from-javascript-to-flask

@app.route("/")
def get_predictions():
    incoming_data = {
        "title": "Dupa sranie jebanie z dupy ĄĄĄąą żźźźóaa że",
        "highligh": "jebanie jebanie w dupe",
        "author": "Jacek dupa"
    }

    cleanedData = dataCleaner(incoming_data).clean()
    features = featureMaker(incoming_data, ['title', 'author'], '/home/jacek/word2vec (1)').process()
    #predictions = modelsHandler().predict_all(features)

    return jsonify(features)


if __name__ == "__main__":
    app.run(debug=True)
