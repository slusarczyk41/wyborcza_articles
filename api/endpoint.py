from app import app
from flask import jsonify, request
from json import loads
from cleaner import dataCleaner
from features import featureMaker
from models import modelContainer


@app.route("/", methods = ['GET', 'POST'])
def get_predictions():
    incomingData = {
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
        incomingData = dict(loads(request.data))
        textColumnsToClean = ['title', 'highlight', 'content', 'media_desc']
        modelsToUse = ['surprise_cat', 'rage_cat', 'joy_cat', 'fear_cat', 'sadness_cat']

        cleanedData = dataCleaner(textColumnsToClean)\
                        .clean(incomingData)
        features = featureMaker('../word2vec', textColumnsToClean)\
                        .process(cleanedData)
        predictions = modelContainer(modelsToUse, textColumnsToClean)\
                        .predict_all(features)

        return jsonify({
            "status": "OK",
            "predictions": predictions
        })
    else:
        return jsonify({
            "status": "ERROR",
            "reason": "data not provided"
        })


if __name__ == "__main__":
    app.run(debug=True)
