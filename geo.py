# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:30:37 2016

@author: enoble
"""

import cl_data
from geopy.distance import great_circle
from math import atan2,degrees,inf

def calc_distance(location, destination):
    # Calculate the great-circle distance between two points
    # Expects two tuples of longlat numbers
    return great_circle(location, destination).miles

def choose_destination(location, places):
    # Calculate the closest place to our current location and remove it
    # from the array of possible places to avoid duplication
    destination = ("", inf)
    for place in set(places):
        distance = int(round(calc_distance(places[location], places[place])))
        if location != place and distance < destination[1]:
            destination = (place, distance)
    return destination

def get_direction(location, destination, places):
    # Get cardinal direction from location to destination
    # Expects two place names (strings) and a corresponding dictionary 
    # of longlat values – {place: (long, lat), etc}
    xDiff = places[destination][0] - places[location][0]
    yDiff = places[destination][1] - places[location][1]
    angle = degrees(atan2(yDiff, xDiff)) + 180
    # Remove location from dictionary so we keep moving forward
    del places[location]
    # Calculate cardinal direction
    if angle <= 22 and angle >= 338:
        return "west"
    elif angle <= 337 and angle >= 293:
        return "northwest"
    elif angle <= 292 and angle >= 248:
        return "north"
    elif angle <= 247 and angle >= 203:
        return "northeast"
    elif angle <= 202 and angle >= 158:
        return "east"
    elif angle <= 157 and angle >= 113:
        return "southeast"
    elif angle <= 112 and angle >= 68:
        return "south"
    else:
        return "southwest"
        
for location in cl_data.place_names[1:]:
    print(calc_distance(cl_data.place_coords[location],
                        cl_data.place_coords[cl_data.place_names[cl_data.place_names.index(location) - 1]]))