import random
from math import atan2, degrees, inf
from typing import Tuple

from geopy.distance import great_circle

import data
from captains import Captain
from ships import OurShip


class RangeDict(dict):
    """
    Enables a dictionary whose keys are ranges.

    Overrides `__getitem__` to handle keys that are ranges.
    """

    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


# Would be quicker to have this as a 360-key dictionary, but this feels neater
CARDINAL_DIRECTIONS = RangeDict(
    {
        range(338, 361): "west",
        range(293, 338): "northwest",
        range(248, 293): "north",
        range(203, 248): "northeast",
        range(158, 203): "east",
        range(113, 158): "southeast",
        range(68, 113): "south",
        range(23, 68): "southwest",
        range(0, 23): "west",
    }
)


def check_wind(captain: Captain) -> Tuple[float, str]:
    """
    Rolls on the wind table to see if this is beneficial or detrimental to sailing.

    Takes a captain object, as certain captain attributes will affect the roll. Returns a tuple
    containing: a floating point number that acts as a speed modifier, and a wind description if
    relevant
    """
    roll = random.randint(0, 100)

    if roll:  # No captain can avoid being becalmed
        roll += captain.navigator / 2  # Better navigators get better rolls
        if roll <= 25:
            return 0.5, ""
        elif roll >= 90:
            return 2.0, random.choice(data.wind_good)
        else:
            return 1.0, ""
    else:
        return 0, random.choice(data.wind_bad)


def calc_distance(location: Tuple[int, int], destination: Tuple[int, int]) -> float:
    """
    Calculate the great-circle distance between two points. Expects two tuples of longlat numbers
    """
    return great_circle(location, destination).miles


def choose_destination(location: str, places: dict, visited: set) -> Tuple[str, float]:
    """
    Calculate the closest place to our current location and make sure we haven't visited it before
    """
    destination = ("", inf)

    for candidate in places:
        distance = int(round(calc_distance(places[location], places[candidate])))
        if (
            location != candidate
            and distance < destination[1]
            and candidate not in visited
        ):
            destination = (candidate, distance)

    return destination


def get_direction(location: str, destination: str, places: dict) -> str:
    """
    Get cardinal direction from location to destination. Expects two place names (strings) and a
    corresponding dictionary of longlat values – {place: (long, lat), etc}
    """
    x_diff = places[destination][0] - places[location][0]
    y_diff = places[destination][1] - places[location][1]

    return CARDINAL_DIRECTIONS[int(degrees(atan2(y_diff, x_diff)) + 180)]


def get_new_heading(
    location: str, all_coords: dict, visited_locations: set
) -> Tuple[str, float, str]:
    """
    Calculates a new destination
    """
    new_destination, new_distance = choose_destination(
        location, all_coords, visited_locations
    )
    new_direction = get_direction(location, new_destination, all_coords)
    log = (
        f"<span>We set sail from {location}, heading {new_direction} "
        f"to {new_destination}. </span>"
    )
    return new_destination, new_distance, log


if __name__ == "__main__":
    # check_wind
    speed, description = check_wind(Captain())
    assert type(speed) is float
    if description:
        assert description in [*data.wind_good, *data.wind_bad]

    # calc_distance
    assert calc_distance((1, 2), (2, 1)) == 97.69549216497437

    # choose_destination
    destination, distance = choose_destination("Tainan", data.place_coords, set())
    assert destination == "Anping", destination
    assert distance == 1, distance

    destination, distance = choose_destination(
        "Tainan", data.place_coords, set(["Anping"])
    )
    assert destination == "Wang-an", destination
    assert distance == 60, distance

    # get_direction
    direction = get_direction("Tainan", "Anping", data.place_coords)
    assert direction == "southeast", direction

    # get_new_heading
    captain = Captain()
    ship = OurShip(captain)
    destination, distance, log = get_new_heading(
        data.place_names[0], data.place_coords, ship.visited
    )
    assert log.startswith("<span>") and log.endswith("</span>")
