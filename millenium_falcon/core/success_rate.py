import copy
from typing import Dict, List, Set

import numpy as np
from loguru import logger

from millenium_falcon.core.loaders import BountyHunter, Falcon, PlanetGraph


class VisitInfo:
    def __init__(self, planet, day, remain_fuel):
        self.planet = planet
        self.day = day
        self.remain_fuel = remain_fuel

    def __str__(self):
        return f"{self.planet}(day:{self.day}, fuel:{self.remain_fuel})"


class FalconSuccessRate:
    def __init__(self, falcon: Falcon):
        self.falcon: Falcon = falcon
        logger.trace(self.falcon)

    def __call__(self, bounty_hunter: BountyHunter) -> float:
        """
        Returns the success rate for the bounty hunter
        :param bounty_hunter: The bounty hunter object containing the countdown and
            the schedule
        :return: Success Probability
        """
        possible_paths = self._generate_possible_paths()
        capture_probability = self._get_min_encounter_capture_probability(
            possible_paths=possible_paths, bounty_hunter=bounty_hunter
        )
        success_rate = round(1 - capture_probability, 2) * 100
        return success_rate

    def explore(
        self,
        dst: str,
        path: List[VisitInfo],
        paths: List[List[VisitInfo]],
        graph: PlanetGraph,
        autonomy: int,
        visited: Set = set(),
    ):
        """
        dst: Destination planet
        path: List of tuples. Each tuple is (current planet, total passed days, fuel days, refueled)
        paths: The final list of paths
        graph: Graph containing the connected planets and the cost
        visited: The visited planets in this path
        """
        assert len(path) != 0, (
            "Path cannot be empty. "
            "Atleast the source should be added when beginning the algo"
        )
        cur_vi: VisitInfo = path[-1]
        if cur_vi.planet == dst:
            paths.append(copy.deepcopy(path))
        else:
            visited.add(cur_vi.planet)
            for neig_planet in graph.routes[cur_vi.planet]:
                if neig_planet not in visited:
                    days_to_reach_nxt_planet: int = graph.travel_time[
                        (cur_vi.planet, neig_planet)
                    ]
                    refuelled = False
                    if cur_vi.remain_fuel < days_to_reach_nxt_planet:
                        # Stay on the same planet on the next day for refuelling
                        logger.trace(f"Refuelling at {cur_vi.planet}")
                        path.append(
                            VisitInfo(
                                planet=cur_vi.planet,
                                day=cur_vi.day + 1,
                                remain_fuel=cur_vi.remain_fuel + self.falcon.autonomy,
                            ),
                        )
                        refuelled = True

                    # Explore ahead by going to the neighbouring planet
                    path.append(
                        VisitInfo(
                            planet=neig_planet,
                            day=path[-1].day + days_to_reach_nxt_planet,
                            remain_fuel=path[-1].remain_fuel - days_to_reach_nxt_planet,
                        )
                    )
                    self.explore(
                        path=path,
                        dst=dst,
                        paths=paths,
                        graph=graph,
                        autonomy=autonomy,
                        visited=visited,
                    )
                    # Backtrack and remove the neighbouring planet from the path
                    path.pop()
                    # Backtrack twice if refueling was required
                    if refuelled:
                        path.pop()

            visited.remove(cur_vi.planet)

    def _generate_possible_paths(self) -> List[List[VisitInfo]]:
        """
        Generate all possible paths for the falcon and the planet system
        """
        paths = []
        starting_point = VisitInfo(
            planet=self.falcon.departure, day=0, remain_fuel=self.falcon.autonomy
        )
        self.explore(
            path=[starting_point],
            dst=self.falcon.arrival,
            paths=paths,
            graph=self.falcon.planet_graph,
            autonomy=self.falcon.autonomy,
        )
        logger.trace("\n" + f"\n".join(["->".join(str(v) for v in p) for p in paths]))
        return paths

    def _get_min_encounter_capture_probability(
        self, possible_paths: List[List[VisitInfo]], bounty_hunter: BountyHunter
    ) -> float:
        """
        The minimum encounter capture probability
        :param possible_paths: List of paths which could be taken
        :param bounty_hunter: The bounty hunter schedule and countdown as
            observed by intercepted data
        :return: Minimum capture probability
        """
        logger.debug(bounty_hunter)
        countdown: int = bounty_hunter.countdown
        min_encounter = np.inf
        for path in possible_paths:
            arrival_day: int = path[-1].day
            if arrival_day <= countdown:
                vi: VisitInfo
                path = self.avoid_bounty_hunters_by_adding_waittime(
                    countdown=countdown,
                    path=path,
                    hunter_schedule=bounty_hunter.schedule,
                )
                encounter = sum(
                    [(vi.day in bounty_hunter.schedule[vi.planet]) for vi in path]
                )
                logger.debug(f"Path - {'->'.join(str(v) for v in path)}")
                logger.debug(f"The number of encounter is: {encounter}")
                min_encounter = min(encounter, min_encounter)
            else:
                logger.debug(
                    f"The path {'->'.join(str(v) for v in path)} cannot be considered"
                    f" as countdown({countdown}) ends before the arrival day{arrival_day}"
                )
        return (
            self._get_probability_of_capture(min_encounter)
            if min_encounter != np.inf
            else 1
        )

    @staticmethod
    def avoid_bounty_hunters_by_adding_waittime(
        countdown: int, path: List[VisitInfo], hunter_schedule: Dict[str, List[int]]
    ) -> List[VisitInfo]:
        """
        Avoid bounty hunters by waiting on planets
        :param countdown: The countdown before Endor is destroyed
        :param path: The list of visited information along the path
        :param hunter_schedule: The hunter schedule containing the days on
            which the bounty hunters are present on a planet
        :result: The new path with added delays to avoid facing bounty hunters
        """
        arrival_day: int = path[-1].day
        delay_budget: int = countdown - arrival_day
        new_path: List[VisitInfo] = []
        delay: int = 0
        if delay_budget == 0:
            return path

        for stop in path:
            if (
                new_path
                and stop.day in hunter_schedule[stop.planet]
                and any(
                    # If staying at least one day allows to avoid the hunter schedule
                    stop.day + day not in hunter_schedule[stop.planet]
                    for day in range(delay_budget + 1)
                )
                and delay_budget != 0
            ):
                while stop.day in hunter_schedule[stop.planet] and delay_budget != 0:
                    new_path.append(
                        VisitInfo(
                            planet=new_path[-1].planet,
                            # Wait for one day at the previous planet
                            day=new_path[-1].day + 1,
                            remain_fuel=new_path[-1].remain_fuel,
                        )
                    )
                    delay_budget -= 1
                    delay += 1

            # Finally visit the planet when the hunters have gone or
            # there is no option (i.e have to visit as cannot delay)
            new_path.append(
                VisitInfo(
                    planet=stop.planet,
                    day=stop.day + delay,
                    remain_fuel=stop.remain_fuel,
                )
            )
        return new_path

    @staticmethod
    def _get_probability_of_capture(encounters: int) -> float:
        """
        :param encounters: The number of encounters with the bounty hunter
        :return: The probability of capture
        """
        result: float = 0.0
        if encounters == 0:
            return result
        for i in range(encounters):
            result += (9 ** i) / (10 ** (i + 1))
        return result
