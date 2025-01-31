import json
from pathlib import Path

from loguru import logger

from millenium_falcon.core.loaders import BountyHunter, Falcon
from millenium_falcon.core.success_rate import FalconSuccessRate
from millenium_falcon.utils import set_loglevel
import sys

def give_me_the_odds():
    millenium_falcon_path, empire_path = sys.argv[1], sys.argv[2]
    falcon = Falcon(Path(millenium_falcon_path))
    get_success_probability = FalconSuccessRate(falcon)
    bounty_hunter = BountyHunter(Path(empire_path))
    success_rate = get_success_probability(bounty_hunter)
    logger.debug(f"Success Rate is: {success_rate}")
    return success_rate