import json
from pathlib import Path

from flask import Flask, render_template, request

import millenium_falcon.configs as configs
from millenium_falcon.core.loaders import BountyHunter, Falcon
from millenium_falcon.core.success_rate import FalconSuccessRate

app = Flask(__name__)
MILLENIUM_FALCON_PATH = "inputs/millennium-falcon.json"


def get_success_probability_fn():
    falcon = Falcon(Path(MILLENIUM_FALCON_PATH))
    return FalconSuccessRate(falcon)


@app.route("/")
def upload_file():
    return render_template("form.html", port=configs.PORT)


@app.route("/uploader", methods=["POST"])
def get_odds_of_success():
    if request.method == "POST":
        intercepted_data = json.load(request.files["intercepted_data"])

        bounty_hunter = BountyHunter(d=intercepted_data)
        success_probability = get_success_probability(bounty_hunter)

        return render_template(
            "result.html",
            intercepted_data=json.dumps(
                intercepted_data, sort_keys=True, indent=4, separators=(",", ": ")
            ),
            success_probability=success_probability,
        )


if __name__ == "__main__":
    get_success_probability = get_success_probability_fn()
    app.run(host="0.0.0.0", port=configs.PORT, debug=True)
