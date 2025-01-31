import json
from pathlib import Path

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

import millenium_falcon.configs as configs
from millenium_falcon.core.loaders import BountyHunter, Falcon
from millenium_falcon.core.success_rate import FalconSuccessRate

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

app.config['CORS_HEADERS'] = 'application/json'

MILLENIUM_FALCON_PATH = "inputs/millennium-falcon.json"


def get_success_probability_fn():
    falcon = Falcon(Path(MILLENIUM_FALCON_PATH))
    return FalconSuccessRate(falcon)


@app.route("/")
@cross_origin(supports_credentials=True)
def upload_file():
    return render_template("form.html", port=configs.PORT)


@app.route("/uploader", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_odds_of_success():
    if request.method == "POST":
        # print(request.json)
        intercepted_data = request.json

        bounty_hunter = BountyHunter(d=intercepted_data)
        success_probability = get_success_probability(bounty_hunter)

        # return render_template(
        #     "result.html",
        #     intercepted_data=json.dumps(
        #         intercepted_data, sort_keys=True, indent=4, separators=(",", ": ")
        #     ),
        #     success_probability=success_probability,
        # )
        return {
            'odds' : success_probability,
            "data" : intercepted_data
        }

if __name__ == "__main__":
    get_success_probability = get_success_probability_fn()
    app.run(host="0.0.0.0", port=configs.PORT, debug=True)



