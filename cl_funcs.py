import random
from math import atan2, degrees, inf
from typing import Tuple

from arrow import Arrow, get
from geopy.distance import great_circle

import cl_data
from captains import Captain


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


def begins_with_vowel(word: str) -> str:
    """
    Returns the correct indefinite article depending on the starting letter of the word
    """
    return "an" if word[0].lower() in "aeiou" else "a"


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
            return 2.0, random.choice(cl_data.wind_good)
        else:
            return 1.0, ""
    else:
        return 0, random.choice(cl_data.wind_bad)


def calc_distance(location: Tuple[int, int], destination: Tuple[int, int]) -> float:
    """
    Calculate the great-circle distance between two points. Expects two tuples of longlat numbers
    """
    return great_circle(location, destination).miles


def choose_destination(location: str, places: dict, visited: list) -> Tuple[str, float]:
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


def get_date(date: Arrow) -> str:
    """
    Formats a date object for inclusion in our output text.
    """
    return f"\n<h3 class='date'>{date.format('MMMM')} {date.format('Do')}, {str(date.year)}</h3>\n"


if __name__ == "__main__":
    # begins_with_vowel
    assert begins_with_vowel("Dog") == "a"
    assert begins_with_vowel("Apple") == "an"

    # check_wind
    speed, description = check_wind(Captain())
    assert type(speed) is float
    if description:
        assert description in [*cl_data.wind_good, *cl_data.wind_bad]

    # calc_distance
    assert calc_distance((1, 2), (2, 1)) == 97.69549216497437

    # choose_destination
    destination, distance = choose_destination("Tainan", cl_data.place_coords, [])
    assert destination == "Anping", destination
    assert distance == 1, distance

    destination, distance = choose_destination(
        "Tainan", cl_data.place_coords, ["Anping"]
    )
    assert destination == "Wang-an", destination
    assert distance == 60, distance

    # get_direction
    direction = get_direction("Tainan", "Anping", cl_data.place_coords)
    assert direction == "southeast", direction

    # get_date
    date = get("1767-01-01", "YYYY-MM-DD")
    formatted = get_date(date)
    assert formatted == "\n<h3 class='date'>January 1st, 1767</h3>\n", formatted
