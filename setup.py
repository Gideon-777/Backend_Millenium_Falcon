from setuptools import setup

setup(
    name="millenium_falcon",
    version="1.0",
    packages=["millenium_falcon"],
    entry_points={
        "console_scripts": ["give-me-the-odds = millenium_falcon.cli:give_me_the_odds"],
    },
)
