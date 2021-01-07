from flask import Flask, request,jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import json


MODEL_PATH = "./nn_model"


def init():
    app = Flask(__name__)

    # set memory utility
    gpu = tf.config.experimental.list_physical_devices('GPU')[0]
    tf.config.experimental.set_memory_growth(gpu, True)

    # load  model
    print("Loading  model...")
    model = load_model(MODEL_PATH)
    print("Model loaded.")


    ##  endpoints  ##
    @app.route("/alive", methods=["GET"])
    def is_alive():
        return jsonify(
            {
                "success": True
            }
        )


    @app.route("/model/predict", methods=["POST"])
    def predict():
        X = np.array(request.json["data"])
        print(X[:2])
        y = model.predict(X).tolist()
        print(y[:2])
        return jsonify({
            "predictions":y
        })


    return app


app = init()


if __name__ == '__main__':
    app.run(port=8003, debug=False)