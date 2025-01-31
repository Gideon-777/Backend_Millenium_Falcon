import json
from pathlib import Path

from loguru import logger

from millenium_falcon.core.loaders import BountyHunter, Falcon
from millenium_falcon.core.success_rate import FalconSuccessRate
from millenium_falcon.utils import set_loglevel

set_loglevel("TRACE")  # For testing
EXAMPLE_PATH = Path("millenium_falcon/tests/examples")


def test_success_rate():
    success = total = 0
    for example_number in ["example1", "example2", "example3", "example4"]:
        logger.info(f"Running the test for {example_number}".upper())
        example_path = EXAMPLE_PATH.joinpath(example_number)
        falcon = Falcon(example_path.joinpath("millennium-falcon.json"))
        get_success_probability = FalconSuccessRate(falcon)

        bounty_hunter = BountyHunter(example_path.joinpath("empire.json"))
        success_rate = get_success_probability(bounty_hunter)
        logger.debug(f"The success rate is: {success_rate}")

        answer = (
            json.loads(example_path.joinpath("answer.json").read_text())["odds"] * 100
        )
        logger.debug(f"The answer is: {answer}")
        if answer == success_rate:
            logger.info("THE TEST HAS PASSED :)")
            success += 1
        else:
            logger.info("THE TEST HAS FAILED :(")
        total += 1

    logger.info(f"Successful Test Count: {success}/{total}")


if __name__ == "__main__":
    test_success_rate()
