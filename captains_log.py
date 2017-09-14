# -*- coding: utf-8 -*-
"""
Created on Tue Sep 5 20:05:40 2017

@author: enoble
"""

import arrow
import codecs
import inflect
import random
import re

import captains
import cl_data
import cl_funcs
import ships

from bs4 import BeautifulSoup


def start():
    """This function initialises a new captain, ship and location"""

    captain = captains.Captain()
    ship = ships.Vessel()
    location = random.choice(cl_data.place_names)
    destination = cl_funcs.choose_destination(location, cl_data.place_coords, [])
    direction = cl_funcs.get_direction(location, destination[0], cl_data.place_coords)

    return (captain,
            ship,
            location,
            destination,
            direction)


def captains_log(wordcount):
    """This function plays the game and outputs a log text of approximate length {wordcount}"""

    log_text = ''
    log_word_count = 0

    doc_head = '''<html>
    <head>
        <title>Captain’s Log</title>
        <meta charset="UTF-8">
        <link rel=\'stylesheet\' type=\'text/css\' href=\'styles.css\'>
        <link href="https://fonts.googleapis.com/css?family=Tangerine:400,700" rel="stylesheet">
    </head>
    <body>'''

    doc_end = '</body>\n</html>'

    parchment_start = '<div class=\'parchment-top\'><div class=\'parchment\'></div><div class=\'parchment-body\'>'
    parchment_end = '</div><div class=\'parchment-bottom\'></div></div>'

    # Python doesn't do well with dates pre-1900, so we use Arrow
    current_date = arrow.get('1767-01-01', 'YYYY-MM-DD')

    # We keep generating luckless captains until we reach {wordcount} words
    while True:

        temp_text = ''

        # Check log_text to see if we're at {wordcount}
        if log_word_count >= wordcount:
            break

        # Track visited places
        visited = []

        # Start the first day
        temp_text += (parchment_start + cl_funcs.get_date(current_date))

        # Initialise objects and places
        (current_captain,
         current_ship,
         current_location,
         current_destination,
         current_direction) = start()

        visited.append(current_location)

        # Add the new captain's first log entry
        temp_text += '<span>My name is ' + current_captain.name + \
                     ', captain of the ' + current_ship.type + ' “' + \
                     current_ship.name + '”. We set sail from ' + \
                     current_location + ', heading ' + current_direction + \
                     ' to ' + current_destination[0] + '. This is my log.</span>\n'

        distance = current_destination[1]

        # Travel
        days_completed = 0

        # We keep travelling until we are destroyed
        while not current_ship.destroyed:

            # We keep travelling towards the destination until we reach it
            while distance > 0:

                # We keep track of the day's entry in case there's nothing interesting
                # to commit to the main log
                day_log_entry = ('\n' + cl_funcs.get_date(current_date) + '<span>')

                # Provisions and rum decrease
                current_ship.provisions -= 1
                current_ship.rum -= (1 + (current_captain.drunkard // 10))

                # If either fall below zero there are consequences
                if current_ship.provisions < 0:
                    current_ship.crew_health -= 20
                    day_log_entry += random.choice(cl_data.provisions_low) + ' '
                elif current_ship.rum < 0:
                    current_ship.crew_sanity -= 20
                    day_log_entry += random.choice(cl_data.rum_low) + ' '

                # Make sure the crew are alive and sane, otherwise start afresh
                if current_ship.crew_health <= 0 or current_ship.crew_sanity <= 0:
                    if current_ship.crew_health <= 0:
                        current_ship.sunk('starvation')
                    else:
                        current_ship.sunk('sobriety')
                    current_ship.destroyed = True
                    day_log_entry += parchment_end + '\n\n<p class=\'ending\'>Thus ends the tale of the “' + \
                                                     current_ship.name + '” and her captain, ' + \
                                                     current_captain.name + \
                                                     ' – lost to either cannibalism or sobriety, pray we never ' + \
                                                     'discover which…</p>'

                    temp_text += day_log_entry

                    break

                # We make a roll against the encounter deck
                encounter = random.randint(1, 100)

                # Sometimes we encounter a hostile vessel
                if encounter > 90:
                    enemy = ships.Enemy(current_ship)
                    day_log_entry += enemy.description + ' '

                    # Not all will risk an attack
                    if enemy.attacking:

                        # If they do we need to see if we die
                        destruction = (enemy.size - current_ship.size) + \
                                      current_captain.fighter - \
                                      current_captain.navigator

                        # If we do, we set the crew health to zero, log a solemn
                        # message and break out of the loop
                        if destruction > 50:
                            current_ship.sunk('combat')
                            current_ship.destroyed = True
                            day_log_entry += parchment_end + '\n\n<p class=\'ending\'>Thus ends the tale of the “' + \
                                                             current_ship.name + '” and her captain, ' + \
                                                             current_captain.name + ' – both lost fighting ' + \
                                                             cl_funcs.begins_with_vowel(enemy.type) + " " + \
                                                             enemy.type + '. All we recovered was this weather-beaten \
                                                             log book…</p>'

                            temp_text += day_log_entry

                            break

                        # If we don't there is rejoicing
                        else:
                            day_log_entry += (random.choice(cl_data.victory) + ' ')

                # If we have survived the encounter deck we calculate the wind
                wind = cl_funcs.check_wind(current_captain)
                distance_travelled = 125 * wind[0]
                days_completed += 1
                current_date = current_date.replace(days=+1)
                distance -= distance_travelled

                # Check if anything interesting happened and add it to the main log
                # if so
                if day_log_entry[-1] != '>':
                    temp_text += (day_log_entry + '</span>')

            # If the distance is less than or equal to zero, we have arrived!
            if not current_ship.destroyed:

                # Initialise the place variables
                personalities = {
                    'good': cl_data.personality_good,
                    'bad': cl_data.personality_bad
                }
                objectsgb = {
                    'good': cl_data.objects_good,
                    'bad': cl_data.objects_bad
                }
                orientation = random.choice(['good', 'bad'])

                # Possible to arrive in less than a day, so need to account for that
                day_text = ''
                p = inflect.engine()
                if days_completed:
                    if days_completed > 1:
                        day_text = p.number_to_words(days_completed) + ' days’'
                    else:
                        day_text = p.number_to_words(days_completed) + ' day’s'
                else:
                    day_text = 'less than a day’s'

                temp_text += '<span>We arrived at ' + current_destination[0] + \
                             ' after ' + day_text + ' sailing. The people here are ' + \
                             random.choice(personalities[orientation]) + \
                             ' and ' + random.choice(personalities[orientation]) + \
                             ', ' + random.choice(cl_data.known_for) + ' for their ' + \
                             random.choice(objectsgb[orientation]) + ' ' + \
                             random.choice(cl_data.objects) + '. </span>'

                # Now we find a new destination
                current_location = current_destination[0]
                if len(visited) == len(set(cl_data.place_coords)) - 1:
                    visited = []
                visited.append(current_location)
                current_destination = cl_funcs.choose_destination(current_location,
                                                                  cl_data.place_coords,
                                                                  visited)
                current_direction = cl_funcs.get_direction(current_location,
                                                           current_destination[0],
                                                           cl_data.place_coords)
                distance = current_destination[1]
                days_completed = 0
                temp_text += cl_funcs.get_date(current_date)
                temp_text += '<span>We set sail from ' + current_location + \
                             ', heading ' + current_direction + ' to ' + \
                             current_destination[0] + '. </span>'
                current_date = current_date.replace(days=+1)

        log_word_count += len(list(filter(None, re.split(r'\s+', re.sub(r'<(.*?)>+', '', temp_text)))))
        log_text += temp_text

    # Print out the stats for this run
    log_text += '\n\n<p class=\'stats\'>You made ' + captains.Captain.return_count() + ', ' + \
                ships.Vessel.return_count() + '</p>'

    # Make the log valid HTML and write it to a file
    log_text = doc_head + log_text + doc_end
    output = codecs.open('output/captains-log.html', 'w', 'utf-8')
    soup = BeautifulSoup(log_text, 'html.parser')
    print(soup.prettify(), file=output)
    output.close()

if __name__ == '__main__':
    count = None
    while not count:
        count = input('Enter an integer wordcount: ')
        try:
            int(count)
            count = int(count)
            break
        except:
            print("{0} isn’t an integer…".format(count))
            count = None

    captains_log(count)
