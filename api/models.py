from app import cache
from joblib import load
from tensorflow.keras.models import load_model


class modelContainer():
    def __init__(self, models_list, columns):
        self.models_list = models_list
        self.model_container = {}
        self.columns = columns

    cache.cached(timeout=3600)
    def read_models(self):
        for model_name in self.models_list:
            self.model_container[model_name] = {
                "pca_vectors" : load('../models/vectors_pca_'+model_name),
                "pca_tfidf"   : load('../models/tfidf_pca_'+model_name),
                "clf_features": load('../models/feature_selection_'+model_name),
                "model"       : load_model('../models/'+model_name),
            }

    def process(self, modelName):
        model = self.model_container[modelName]
        return [
            self.features["dummy_dates"] +
            self.features["author_dummy"] +
            self.features["division_dummy"] +
            self.features["media_type_dummy"] +
            model["pca_vectors"]["content"]\
                .transform([self.features["vectors"]["content"]])[0].tolist() +
            model["pca_vectors"]["highlight"]\
                .transform([self.features["vectors"]["highlight"]])[0].tolist() +
            model["pca_vectors"]["title"]\
                .transform([self.features["vectors"]["title"]])[0].tolist() +
            model["pca_vectors"]["media_desc"]\
                .transform([self.features["vectors"]["media_desc"]])[0].tolist() +
            model["pca_tfidf"]\
                    .transform([self.features["tf_idf"]])[0].tolist()
        ]

    def predict_all(self, features):
        if self.model_container == {}:
            self.read_models()
        self.features = features

        pretidctions = {}
        for model in self.models_list:
            processedFeatures = self.process(model)
            pca = self.model_container[model]["clf_features"]
            selectedFeatures = pca.transform(processedFeatures)
            tensorflowObj = self.model_container[model]["model"]
            modelPrediction = tensorflowObj.predict(selectedFeatures)
            if float(modelPrediction[0][0]) > 0.6:
                pretidctions[model] = "reaction"
            elif float(modelPrediction[0][0]) < 0.4:
                pretidctions[model] = "no_reaction"
            else:
                "ambigious"
        return pretidctions
