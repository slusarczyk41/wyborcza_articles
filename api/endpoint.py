from app import app

from flask import jsonify, request
from json import loads
from cleaner import dataCleaner
from features import featureMaker
# from models import modelsHandler
# https://stackoverflow.com/questions/53042856/how-can-i-pass-a-dictionary-from-javascript-to-flask

@app.route("/", methods = ['GET', 'POST'])
def get_predictions():
    incoming_data = {
        "title": "Dupa sranie jebanie z dupy ĄĄĄąą żźźźóaa że",
        "content": "jebanie jebanie w dupe",
        "author": "Jacek dupa",
        "highlight": "Pupa",
        "author": "swiat",
        "division": "swiat",
        "media_desc": "gowno jakies",
        "media": "image",
        "date": "16 lipca 2019 | 12:00"
    }
    if request.data:
        incoming_data = dict(loads(request.data))

    cleanedData = dataCleaner(incoming_data).clean()
    features = featureMaker(incoming_data, '/home/jacek/word2vec_test').process()
    #predictions = modelsHandler().predict_all(features)
    #return jsonify(features)
    return "DUZOxD"


if __name__ == "__main__":
    app.run(debug=True)
