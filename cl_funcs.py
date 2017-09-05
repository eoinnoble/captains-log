# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 14:32:40 2016

@author: enoble
"""

import random

import cl_data

from math import atan2, degrees, inf
from geopy.distance import great_circle


# Handle a dictionary whose keys are ranges
class RangeDict(dict):

    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


# Would be quicker to have this as a 360-key dictionary, but this feels neater
cardinals = RangeDict({
    range(338, 361): "west",
    range(293, 338): "northwest",
    range(248, 293): "north",
    range(203, 248): "northeast",
    range(158, 203): "east",
    range(113, 158): "southeast",
    range(68, 113):  "south",
    range(23, 68):   "southwest",
    range(0, 23):    "west"
})


def begins_with_vowel(word):
    """Returns the correct indefinite article depending on the starting letter of the word"""

    return 'an' if word[0].lower() in 'aeiou' else 'a'


def check_wind(captain):
    """Rolls on the wind table to see if this is beneficial or detrimental to sailing.

    Takes a captain object, as certain captain attributes will affect the roll. Returns a tuple containing:
    a floating point number that acts as a speed modifier, and a wind description if relevant"""

    roll = random.randint(0, 100)

    if roll:                            # No captain can avoid being becalmed
        roll += captain.navigator / 2   # Better navigators get better rolls
        if roll <= 25:
            return 0.5, ''
        elif roll >= 90:
            return 2.0, random.choice(cl_data.wind_good)
        else:
            return 1.0, ''
    else:
        return 0, random.choice(cl_data.wind_bad)


def calc_distance(location, destination):
    """Calculate the great-circle distance between two points. Expects two tuples of longlat numbers"""

    return great_circle(location, destination).miles


def choose_destination(location, places, visited):
    """Calculate the closest place to our current location and make sure we haven't visited it before"""

    destination = ("", inf)

    for place in set(places):
        distance = int(round(calc_distance(places[location], places[place])))
        if location != place and distance < destination[1] and place not in visited:
            destination = (place, distance)

    return destination


def get_direction(location, destination, places):
    """Get cardinal direction from location to destination. Expects two place names (strings) and a corresponding
    dictionary of longlat values – {place: (long, lat), etc}"""

    x_diff = places[destination][0] - places[location][0]
    y_diff = places[destination][1] - places[location][1]

    # Return a cardinal direction
    angle = degrees(atan2(y_diff, x_diff)) + 180
    return cardinals[int(degrees(atan2(y_diff, x_diff)) + 180)]


def get_date(date):

    return ('\n<h3 class=\'date\'>' + date.format('MMMM') + ', ' +
            str(date.year) + '</h3>\n')


if __name__ == '__main__':
    assert begins_with_vowel('Dog') == 'a'
    assert begins_with_vowel('Apple') == 'an'
