# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 14:32:40 2016

@author: enoble
"""

import arrow, codecs, io, random, re
import captains, cl_data, ships
from bs4 import BeautifulSoup
from geopy.distance import great_circle
from math import atan2,degrees,inf


# Check if word begins with a vowel
def begins_with_vowel(word):
    if word[0] in "aeiouAEIOU":
        return "an"
    else:
        return "a"

def get_file(file_name):
    '''Takes a file name (string), reads the file line by line and saves it to 
       a list, which it then returns.
       
       Needs the io module to be imported.
       '''
    with io.open(file_name, "r", encoding = "utf-8") as my_file:
        return my_file.read().split("\n")

def check_wind(captain):
    '''Rolls on the wind table to see if this is beneficial or detrimental
       to sailing. Takes a captain object, as certain captain attributes will
       affect the roll. Returns a tuple containing: a floating point number that 
       acts as a speed modifier, and a wind description if relevant'''
    roll = random.randint(0, 100)
    if roll: # No captain can avoid being becalmed
        roll += captain.navigator / 2 # Better navigators get better rolls
        if roll <= 25:
            return (0.5, "")
        elif roll >= 90:
            return (2.0, random.choice(cl_data.wind_good))
        else:
            return (1.0, "")
    else:
        return (0, random.choice(cl_data.wind_bad))
        
def calc_distance(location, destination):
    # Calculate the great-circle distance between two points
    # Expects two tuples of longlat numbers
    return great_circle(location, destination).miles

def choose_destination(location, places, visited):
    # Calculate the closest place to our current location and make sure
    # we haven't visited it before
    destination = ("", inf)
    for place in set(places):
        distance = int(round(calc_distance(places[location], places[place])))
        if location != place and distance < destination[1] and place not in visited:
            destination = (place, distance)
    return destination

def get_direction(location, destination, places):
    # Get cardinal direction from location to destination
    # Expects two place names (strings) and a corresponding dictionary 
    # of longlat values – {place: (long, lat), etc}
    xDiff = places[destination][0] - places[location][0]
    yDiff = places[destination][1] - places[location][1]
    angle = degrees(atan2(yDiff, xDiff)) + 180
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
        
def start():
    captain = captains.Captain()
    ship = ships.Ship()
    location = random.choice(cl_data.place_names)
    destination = choose_destination(location, cl_data.place_coords, [])
    direction = get_direction(location, destination[0], cl_data.place_coords)
    return (captain, 
            ship, 
            location, 
            destination, 
            direction)

def captains_log():
    """ This function plays the game and outputs a log text """
    
    log_text = """<html>
    <head>
        <title>Captain’s Log</title>
        <link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\">
    </head>
    <body>"""
    soup = BeautifulSoup(log_text, "html.parser")
    # Python doesn't do well with dates pre-1900, so we use Arrow
    current_date = arrow.get('1767-01-01', 'YYYY-MM-DD')
    def get_date():
        """ Kept having to do this, so abstracted it to a function """
        return ("\n<h3 class=\"date\">" + current_date.format('MMMM') + ", " + \
                     str(current_date.year) + "</h3>\n")
    
    # We keep generating luckless captains until we reach 50,000 words
    while len(re.split(r'[^0-9A-Za-z]+', soup.get_text())) < 55000:
        soup = BeautifulSoup(log_text, "html.parser")
        # No captain should revisit a place they've already been, so we keep
        # track of visited place names in this list
        visited= []

        parchment_start = "<div class=\"parchment-top\"><div class=\"parchment\"></div><div class=\"parchment-body\">"
        parchment_end = "</div><div class=\"parchment-bottom\"></div></div>"

        # Sometimes captains die immediately, I'm not sure why yet
        if log_text[-6:] != "<body>" and log_text[-4:] != "</p>" and log_text[-12:] != "</div></div>":
            log_text += parchment_end
        
        # Start the first day
        log_text += (parchment_start + get_date())
        
        # Initialise objects and places
        (current_captain, 
         current_ship, 
         current_location, 
         current_destination, 
         current_direction) = start()
        visited.append(current_location)
        
        # Add the new captain's first log entry
        log_text += ("<span>My name is " + current_captain.name + \
                     ", captain of the " + current_ship.type + " “" + \
                     current_ship.name + "”. We set sail from " + \
                     current_location + ", heading " + current_direction + \
                     " to " + current_destination[0] + ". This is my log.</span>\n") 
                     
        distance = current_destination[1]
        
        # Travel
        days_completed = 0
        
        # We keep travelling until we are destroyed
        while not current_ship.destroyed:
            # We keep travelling towards the destination until we reach it
            while distance > 0:
                # We keep track of the day's entry in case there's nothing interesting
                # to commit to the main log
                day_log_entry = ("\n" + get_date() + "<span>")  
                
                # Provisions and rum decrease
                current_ship.provisions -= 1
                current_ship.rum -= (1 + (current_captain.drunkard // 10))
                    
                # If either fall below zero there are consequences
                if current_ship.provisions < 0:
                    current_ship.crew_health -= 20
                    day_log_entry += random.choice(cl_data.provisions_low) + " "
                elif current_ship.rum < 0:
                    current_ship.crew_health -= 20
                    day_log_entry += random.choice(cl_data.rum_low) + " "
            
                # Make sure the crew are alive and sane, otherwise start afresh
                if current_ship.crew_health <= 0 or current_ship.crew_sanity <= 0:
                    current_ship.destroyed = True
                    log_text += parchment_end + "\n\n<p class=\"ending\">Thus ends the tale of the “" + \
                                current_ship.name + "” and her captain, " + \
                                current_captain.name + \
                                " – lost to either cannibalism or sobriety, pray we never discover which…</p>"
                    break
                
                # We make a roll against the encounter deck
                encounter = random.randint(1, 100)
                
                # Sometimes we encounter a hostile vessel
                if encounter > 90:
                    enemy = ships.Enemy(current_ship)
                    day_log_entry += enemy.description + " "
                    
                    # Not all will risk an attack
                    if enemy.attacking:
                        # If they do we need to see if we die
                        destruction = (enemy.size - current_ship.size) + \
                                               current_captain.fighter - \
                                               current_captain.navigator
                        # If we do, we set the crew health to zero, log a solemn 
                        # message and break out of the loop
                        if destruction > 50:
                            current_ship.destroyed = True
                            day_log_entry += parchment_end + "\n\n<p class=\"ending\">Thus ends the tale of the “" + \
                                             current_ship.name + "” and her captain, " + \
                                             current_captain.name + " – both lost fighting a " + \
                                             enemy.type + ". All we recovered was this weather-beaten log book…</p>"
                            break
                        # If we don't there is rejoicing
                        else:
                            day_log_entry += (random.choice(cl_data.victory) + " ")
                
                # If we have survived the encounter deck we calculate the wind
                wind = check_wind(current_captain)           
                distance_travelled = 125 * wind[0]
                days_completed += 1
                current_date = current_date.replace(days=+1)
                distance -= distance_travelled
                
                
                # Check if anything interesting happened and add it to the main log
                # if so
                if day_log_entry[-1] != ">":
                    log_text += (day_log_entry + "</span>")
            
            # If the distance is less than or equal to zero, we have arrived!
            if not current_ship.destroyed:
                # Initialise the place variables
                personalities = {
                    "good": cl_data.personality_good,
                    "bad": cl_data.personality_bad
                }
                objectsgb = {
                    "good": cl_data.objects_good,
                    "bad": cl_data.objects_bad
                }
                orientation = random.choice(["good", "bad"])
                log_text += "<span>We arrived at " + current_destination[0] + \
                            " after " + str(days_completed) + " days’ sailing. The people here are " + \
                            random.choice(personalities[orientation]) + \
                            " and " + random.choice(personalities[orientation]) + \
                            ", " + random.choice(cl_data.known_for) + " for their " + \
                            random.choice(objectsgb[orientation]) + " " + \
                            random.choice(cl_data.objects) + ". </span>"
                
                # Now we find a new destination
                current_location = current_destination[0]
                if len(visited) == len(set(cl_data.place_coords)) - 1:
                    visited = []
                visited.append(current_location)
                current_destination = choose_destination(current_location, 
                                                         cl_data.place_coords,
                                                         visited)
                current_direction = get_direction(current_location, 
                                                  current_destination[0], 
                                                  cl_data.place_coords)
                distance = current_destination[1]
                days_completed = 0
                log_text += get_date()
                log_text += "<span>We set sail from " + current_location + \
                            ", heading " + current_direction + " to " + \
                            current_destination[0] + ". </span>"     
                current_date = current_date.replace(days=+1) 
    # Make the log valid HTML and write it to a file
    log_text += "</body>\n</html>"
    output = codecs.open("output/captains-log.html", "w", "utf-8")
    print(soup.prettify(), file = output)
    output.close()
                    
            
            