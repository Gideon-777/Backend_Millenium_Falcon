import copy
import json
import sqlite3
from collections import defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np
from loguru import logger

from millenium_falcon import configs


class PlanetGraph:
    def __init__(self, db_path: Path):
        self.planets = set()
        self.routes = defaultdict(list)
        self.travel_time = {}

        for orgin, destination, travel_time in self._get_routes(db_path):
            self._add_route(orgin, destination, travel_time)

    def _add_route(self, origin, destination, travel_time):
        self.planets.add(origin)
        self.planets.add(destination)
        self.routes[origin].append(destination)
        self.routes[destination].append(origin)
        self.travel_time[(origin, destination)] = self.travel_time[
            (destination, origin)
        ] = travel_time
        logger.trace(
            f"Successfully added {origin} -> {destination} in time {travel_time}"
        )

    @staticmethod
    def _get_routes(db_path: Path):
        logger.debug(f"Loading the database from {db_path.absolute()}")
        assert db_path.exists(), f"{db_path} doesnot exists"
        conn = sqlite3.connect(db_path)
        logger.debug("Successfully connected to the database")
        cur = conn.cursor()
        return cur.execute("SELECT origin, destination, travel_time FROM routes")

    def __str__(self):
        return f"""Planets: {','.join(self.planets)}\nRoutes: {json.dumps(self.routes, indent =4)}\nTravel Times: {self.travel_time}"""


class Falcon:
    def __init__(self, millenium_falcon_path: Path):
        assert millenium_falcon_path.exists()
        d = json.loads(millenium_falcon_path.read_text())
        self.departure = d["departure"]
        self.arrival = d["arrival"]
        self.autonomy = d["autonomy"]
        route_db_path = millenium_falcon_path.parent.joinpath(d["routes_db"])
        logger.debug(f"Route Database Path: {route_db_path}")
        self.planet_graph = PlanetGraph(route_db_path)

    def __str__(self):
        return f"Departure: {self.departure}\nArrival: {self.arrival}\nAutonomy: {self.autonomy}\nPlanet Graph: {self.planet_graph}"


class BountyHunter:
    def __init__(self, empire_path: Path = None, d: Dict = None):
        if empire_path is not None:
            assert empire_path.exists()
            d = json.loads(empire_path.read_text())
        assert d is not None
        self.countdown: int = d["countdown"]
        self.schedule = defaultdict(list)
        for bh in d["bounty_hunters"]:
            self.schedule[bh["planet"]].append(bh["day"])
        logger.debug("Successfully loaded the bounty hunters schedule")

    def __str__(self):
        return f"Countdown: {self.countdown}\nBounty Hunter Schedule: {json.dumps(self.schedule, indent = 4)}"


if __name__ == "__main__":
    pass
