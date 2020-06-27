import codecs
import random
import re
import textwrap
from typing import Tuple

import arrow
import inflect
from bs4 import BeautifulSoup

import captains
import cl_data
import cl_funcs
import ships


FONT = "https://fonts.googleapis.com/css?family=Tangerine:400,700"
DOC_HEAD = textwrap.dedent(
    f"""\
    <html>
        <head>
            <title>Captain’s Log</title>
            <meta charset="UTF-8">
            <link rel='stylesheet' type='text/css' href='styles.css'>
            <link href='{FONT}' rel='stylesheet'>
        </head>
        <body>
    """
)
DOC_END = textwrap.dedent(
    """\
    </body>
    </html>
    """
)
PARCHMENT_START = textwrap.dedent(
    """\
    <div class='parchment'>
        <div class='parchment-top'></div>
        <div class='parchment-body'>
    """
)
PARCHMENT_END = textwrap.dedent(
    """</span>
        </div>
        <div class='parchment-bottom'></div>
    </div>
    """
)
# Initialise the place variables
PERSONALITIES = {
    "good": cl_data.personality_good,
    "bad": cl_data.personality_bad,
}
OBJECTS = {
    "good": cl_data.objects_good,
    "bad": cl_data.objects_bad,
}


def start() -> Tuple[
    captains.Captain, ships.Vessel, str, Tuple[str, float], str, str,
]:
    """
    This function initialises a new captain, ship and location
    """
    captain = captains.Captain()
    ship = ships.Vessel(captain=captain)
    location: str = random.choice(cl_data.place_names)
    destination = cl_funcs.choose_destination(location, cl_data.place_coords, [])
    direction = cl_funcs.get_direction(location, destination[0], cl_data.place_coords)
    ship.visited.append(location)
    first_log = (
        f"<span>My name is {captain.name}, captain of the {ship.type} "
        f"“{ship.name}”. We set sail from {location}, heading "
        f"{direction} to {destination[0]}. This is my log.</span>"
    )

    return (captain, ship, location, destination, direction, first_log)


def handle_provisions(ship: ships.Vessel) -> Tuple[bool, str]:
    """
    Handles the provisions for `ship`.

    Returns a boolean denoting whether the ship was destroyed and a `log`
    """
    log = ""
    ship.provisions -= 1
    ship.rum -= 1 + (ship.captain.drunkard // 10)

    if ship.provisions < 0:
        ship.crew_health -= 20
        log += f"{random.choice(cl_data.provisions_low)} "
    elif ship.rum < 0:
        ship.crew_sanity -= 20
        log += f"{random.choice(cl_data.rum_low)} "

    # Make sure the crew are alive and sane...
    if ship.destroyed:
        if ship.crew_health <= 0:
            ship.sink("starvation")
        else:
            ship.sink("sobriety")
        log += (
            f"{PARCHMENT_END}\n\n<p class='ending'>Thus ends the tale of the "
            f"“{ship.name}” and her captain, {ship.captain.name}"
            " – lost to either cannibalism or sobriety, pray we never "
            "discover which…</p>"
        )
        return True, log

    return False, log


def do_encounter(ship: ships.Vessel) -> Tuple[bool, str]:
    """
    Calculates which encounter the `ship` should have and then delegates to the relevant handler
    """
    # We make a roll against the encounter deck
    encounter = random.randint(1, 100)

    # Sometimes we encounter a hostile vessel
    if encounter > 90:
        return do_combat_encounter(ship)
    else:
        return False, ""


def do_combat_encounter(ship: ships.Vessel) -> Tuple[bool, str]:
    """
    Handles combat encounters for `ship`.

    Returns a boolean denoting whether the ship was destroyed and a `log`
    """
    enemy = ships.Enemy(ship)
    log = f"{enemy.description} "

    if enemy.attacking:
        # Let's see if we die
        destruction = (
            (enemy.size - ship.size) + ship.captain.fighter - ship.captain.navigator
        )

        # If we do, we set the crew health to zero, log a solemn
        # message and break out of the loop
        if destruction > 50:
            ship.sink("combat")
            log += (
                f"{PARCHMENT_END}\n\n<p class='ending'>Thus ends the tale of the "
                f"“{ship.name}” and her captain, {ship.name} "
                f"– both lost fighting {cl_funcs.begins_with_vowel(enemy.type)} "
                f"{enemy.type}. All we recovered was this weather-beaten log "
                "book…</p>"
            )
            return True, log

        # If we don't there is rejoicing!
        else:
            log += f"{random.choice(cl_data.victory)} "
            return False, log
    else:
        return False, log


def do_location(
    ship: ships.Vessel, destination: str, days_to_get_here: int, all_locations: list
) -> str:
    """
    Generates the text for a given `destination`.

    As a side effect also updated the `visited` attribute for `ship`
    """
    if len(ship.visited) == len(set(all_locations)) - 1:
        # Against all odds this ship has survived for so long it has visited all the
        # places -- time to visit them all again!
        ship.visited = []
    ship.visited.append(destination)

    orientation = random.choice(["good", "bad"])
    day_text = ""
    p = inflect.engine()

    if days_to_get_here:  # Possible to arrive in less than a day
        if days_to_get_here > 1:
            day_text = f"{p.number_to_words(days_to_get_here)} days’"
        else:
            day_text = f"{p.number_to_words(days_to_get_here)} day’s"
    else:
        day_text = "less than a day’s"

    return (
        f"<span>We arrived at {destination} after {day_text} sailing. "
        f"The people here are {random.choice(PERSONALITIES[orientation])} and "
        f"{random.choice(PERSONALITIES[orientation])}, "
        f"{random.choice(cl_data.known_for)} for their "
        f"{random.choice(OBJECTS[orientation])} "
        f"{random.choice(cl_data.objects)}. </span>"
    )


def find_new_destination(
    location: str, all_coords: dict, visited_locations: list, date: arrow.Arrow
) -> Tuple[str, float, str]:
    """
    Calculates a new destination
    """
    new_destination, new_distance = cl_funcs.choose_destination(
        location, all_coords, visited_locations
    )
    new_direction = cl_funcs.get_direction(location, new_destination, all_coords)
    # log = cl_funcs.get_date(date)
    log = (
        f"<span>We set sail from {location}, heading {new_direction} "
        f"to {new_destination}. </span>"
    )
    return new_destination, new_distance, log


def get_word_count(text: str) -> int:
    """
    Returns number of words in `text` minus HTML element tags
    """
    return len(list(filter(None, re.split(r"\s+", re.sub(r"<(.*?)>+", "", text)))))


def captains_log(word_count: int):
    """
    This function plays the game and outputs a log text of approximate length `word_count`
    """
    TEXT_TO_BE_LOGGED = ""
    log_word_count = 0

    # Python doesn't do well with dates pre-1900, so we use Arrow
    current_date = arrow.get("1767-01-01", "YYYY-MM-DD")

    # We keep generating luckless captains until we reach {word_count} words
    while True:
        if log_word_count >= word_count:
            break

        CAPTAIN_TEXT = ""

        # Start the first day
        CAPTAIN_TEXT += PARCHMENT_START + cl_funcs.get_date(current_date)

        # Initialise objects and places
        (
            current_captain,
            current_ship,
            current_location,
            current_destination,
            current_direction,
            first_log,
        ) = start()

        CAPTAIN_TEXT += first_log
        distance = current_destination[1]
        days_completed = 0

        # We keep travelling until we are destroyed
        while not current_ship.destroyed:

            date_already_logged = False

            # We keep travelling towards the destination until we reach it
            while distance > 0:

                # We keep track of the day's entry in case there's nothing interesting
                # to commit to the main log
                day_log_entry = "<span>"

                sunk, provision_log = handle_provisions(current_ship)
                day_log_entry += provision_log
                if sunk:
                    CAPTAIN_TEXT += day_log_entry
                    break

                sunk, encounter_log = do_encounter(current_ship)
                day_log_entry += encounter_log
                if sunk:
                    CAPTAIN_TEXT += day_log_entry
                    break

                # If we have survived the encounter deck we calculate the wind
                wind = cl_funcs.check_wind(current_captain)
                distance_travelled = 125 * wind[0]
                days_completed += 1
                current_date = current_date.shift(days=+1)
                distance -= distance_travelled

                # Check if anything interesting happened and add it to the main log if so
                if not day_log_entry == "<span>":
                    CAPTAIN_TEXT += f"\n{cl_funcs.get_date(current_date)}"
                    CAPTAIN_TEXT += f"{day_log_entry}</span>"
                    date_already_logged = True

            # If the distance is less than or equal to zero, we have arrived!
            if current_ship.destroyed:
                break

            if not date_already_logged:
                CAPTAIN_TEXT += f"\n{cl_funcs.get_date(current_date)}"
                date_already_logged = True

            CAPTAIN_TEXT += do_location(
                current_ship,
                current_destination[0],
                days_completed,
                cl_data.place_names,
            )

            # these variable names suck
            new_destination, new_distance, destination_log = find_new_destination(
                current_destination[0],
                cl_data.place_coords,
                current_ship.visited,
                current_date,
            )
            CAPTAIN_TEXT += destination_log
            current_date = current_date.shift(days=+1)

            # Re-initialise variables
            days_completed = 0
            current_destination = (new_destination, distance)
            distance = new_distance
            date_already_logged = False

        log_word_count += get_word_count(CAPTAIN_TEXT)
        TEXT_TO_BE_LOGGED += CAPTAIN_TEXT

    # Print out the stats for this run
    TEXT_TO_BE_LOGGED += (
        f"\n\n<p class='stats'>You made {captains.Captain.format_num_instances()}, and lost:</p>"
        f"{ships.Vessel.format_num_instances()}"
    )

    print(TEXT_TO_BE_LOGGED)

    # Make the log valid HTML and write it to a file
    with codecs.open("output/captains-log.html", "w", "utf-8") as output:
        TEXT_TO_BE_LOGGED = DOC_HEAD + TEXT_TO_BE_LOGGED + DOC_END
        soup = BeautifulSoup(TEXT_TO_BE_LOGGED, "html.parser")
        print(soup.prettify(), file=output)


if __name__ == "__main__":
    count = 0
    while not count:
        try:
            count = int(input("Enter an integer word_count: "))
        except ValueError:
            print(f"{count} isn’t an integer…")
            count = 0
        else:
            break

    captains_log(count)
