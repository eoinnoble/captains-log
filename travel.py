import itertools
import random
from typing import Tuple

import inflect
from arrow import Arrow, get

import data
import markup
import navigation
from captains import Captain
from ships import EnemyShip, OurShip
from utils import begins_with_vowel


PERSONALITIES = {
    "good": data.personality_good,
    "bad": data.personality_bad,
}
OBJECTS = {
    "good": data.objects_good,
    "bad": data.objects_bad,
}
PROVISIONS_LOW = itertools.cycle(data.provisions_low)
RUM_LOW = itertools.cycle(data.rum_low)


def get_date(date: Arrow) -> str:
    """
    Formats a date object for inclusion in our output text.
    """
    return f"\n<h3 class='date'>{date.format('MMMM')} {date.format('Do')}, {str(date.year)}</h3>\n"


def generate_captain() -> Tuple[Captain, OurShip, str, float, str, str]:
    """
    This function initialises a new captain, ship and location
    """
    captain = Captain()
    ship = OurShip(captain=captain)
    location: str = random.choice(data.place_names)
    destination, distance = navigation.choose_destination(
        location, data.place_coords, set()
    )
    direction = navigation.get_direction(location, destination, data.place_coords)
    ship.visited.add(location)
    first_log = (
        f"<span>My name is {captain.name}, captain of the {ship.type} "
        f"“{ship.name}”. We set sail from {location}, heading "
        f"{direction} to {destination}. This is my log.</span>"
    )

    return (captain, ship, destination, distance, direction, first_log)


def handle_provisions(ship: OurShip) -> Tuple[bool, str]:
    """
    Handles the provisions for `ship`.

    Returns a boolean denoting whether the ship was destroyed and a `log`
    """
    log = ""
    ship.provisions -= 1
    ship.rum -= 1 + (ship.captain.drunkard // 10)

    if ship.provisions < 0:
        ship.crew_health -= 20
        log += f"{next(PROVISIONS_LOW)} "
    elif ship.rum < 0:
        ship.crew_sanity -= 20
        log += f"{next(RUM_LOW)} "

    # Make sure the crew are alive and sane...
    if ship.destroyed:
        if ship.crew_health <= 0:
            ship.sink("starvation")
        else:
            ship.sink("sobriety")
        log += (
            f"{markup.parchment_end}\n\n<p class='ending'>Thus ends the tale of the "
            f"“{ship.name}” and her captain, {ship.captain.name}"
            " – lost to either cannibalism or sobriety, pray we never "
            "discover which…</p>"
        )
        return True, log

    return False, log


def do_encounter(ship: OurShip) -> Tuple[bool, str]:
    """
    Calculates which encounter the `ship` should have and then delegates to the relevant handler
    """
    # We make a roll against the encounter deck
    encounter = random.randint(1, 100)

    # Sometimes we encounter a hostile OurShip
    if encounter > 90:
        return do_combat_encounter(ship)
    else:
        return False, ""


def do_combat_encounter(ship: OurShip) -> Tuple[bool, str]:
    """
    Handles combat encounters for `ship`.

    Returns a boolean denoting whether the ship was destroyed and a `log`
    """
    enemy = EnemyShip(ship)
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
                f"{markup.parchment_end}\n\n<p class='ending'>Thus ends the tale of the "
                f"“{ship.name}” and her captain, {ship.name} "
                f"– both lost fighting {begins_with_vowel(enemy.type)} "
                f"{enemy.type}. All we recovered was this weather-beaten log "
                "book…</p>"
            )
            return True, log

        # If we don't there is rejoicing!
        else:
            log += f"{random.choice(data.victory)} "
            return False, log
    else:
        return False, log


def do_location(
    ship: OurShip, destination: str, days_to_get_here: int, all_locations: list
) -> str:
    """
    Generates the text for a given `destination`.

    As a side effect also updated the `visited` attribute for `ship`
    """
    if len(ship.visited) == len(set(all_locations)):
        # Against all odds this ship has survived for so long it has visited all the
        # places -- time to visit them all again!
        ship.visited = set()
    ship.visited.add(destination)

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
        f"{random.choice(data.known_for)} for their "
        f"{random.choice(OBJECTS[orientation])} "
        f"{random.choice(data.objects)}. </span>"
    )


def do_travel(
    distance: float, ship: OurShip, days_spent: int, date: Arrow
) -> Tuple[str, bool]:
    """
    Performs the travelling part of our journey, will mutate `date` as a side effect

    Returns a log entry and a boolean denoting whether the current date has already been logged
    """
    log = ""
    date_already_logged = False

    while distance > 0:
        day_log_entry = "<span>"

        sunk, provision_log = handle_provisions(ship)
        day_log_entry += provision_log
        if sunk:
            log += day_log_entry
            return log, date_already_logged

        sunk, encounter_log = do_encounter(ship)
        day_log_entry += encounter_log
        if sunk:
            log += day_log_entry
            return log, date_already_logged

        wind = navigation.check_wind(ship.captain)
        distance_travelled = 125 * wind[0]
        days_spent += 1
        current_date = date.shift(days=+1)
        distance -= distance_travelled

        # Check if anything interesting happened and add it to the main log if so
        if day_log_entry != "<span>":
            log += f"\n{get_date(current_date)}"
            log += f"{day_log_entry}</span>"
            date_already_logged = True

    return log, date_already_logged


def run_captain(
    distance: float,
    ship: OurShip,
    days_spent: int,
    date: Arrow,
    initial_destination: str,
) -> str:
    """
    Simulate the entire lifetime of a captain and their ship, returning a log of their endeavours
    """
    log = ""
    destination = initial_destination

    while not ship.destroyed:
        date_already_logged = False

        travel_log, date_already_logged = do_travel(distance, ship, days_spent, date)
        log += travel_log

        # We have arrived!
        if ship.destroyed:
            return log

        if not date_already_logged:
            log += f"\n{get_date(date)}"

        location_log = do_location(ship, destination, days_spent, data.place_names,)
        (new_destination, new_distance, destination_log,) = navigation.get_new_heading(
            destination, data.place_coords, ship.visited,
        )
        log += location_log
        log += destination_log

        # Re-initialise variables
        date = date.shift(days=+1)
        days_spent = 0
        destination = new_destination
        distance = new_distance
        date_already_logged = False

    return log


if __name__ == "__main__":
    # get_date
    date = get("1767-01-01", "YYYY-MM-DD")
    formatted = get_date(date)
    assert formatted == "\n<h3 class='date'>January 1st, 1767</h3>\n", formatted

    # start
    (captain, ship, destination, distance, direction, log) = generate_captain()
    assert destination in data.place_names, destination
    assert direction in navigation.CARDINAL_DIRECTIONS.values(), direction
    assert log.startswith("<span>") and log.endswith("</span>"), log

    # handle_provisions
    captain = Captain()
    ship = OurShip(captain)
    ship.provisions = 0
    ship.crew_health = 20
    sunk, log = handle_provisions(ship)
    assert sunk is True, sunk
    assert "<p class='ending'>" in log, log
    assert ship.sinkings["sobriety"] == 0, ship.sinkings
    assert ship.sinkings["starvation"] == 1, ship.sinkings

    captain = Captain()
    ship = OurShip(captain)
    ship.rum = 0
    ship.crew_sanity = 20
    sunk, log = handle_provisions(ship)
    assert sunk is True, sunk
    assert "<p class='ending'>" in log, log
    assert ship.sinkings["sobriety"] == 1, ship.sinkings
    assert ship.sinkings["starvation"] == 1, ship.sinkings

    captain = Captain()
    ship = OurShip(captain)
    sunk, log = handle_provisions(ship)
    assert sunk is False, sunk
    assert "<p class='ending'>" not in log, log
    assert ship.sinkings["sobriety"] == 1, ship.sinkings
    assert ship.sinkings["starvation"] == 1, ship.sinkings

    # do_combat_encounter
    captain = Captain()
    captain.fighter = 100
    captain.navigator = 0
    ship = OurShip(captain)
    ship.size = -1
    sunk, log = do_combat_encounter(ship)
    assert sunk is True, sunk
    assert "<p class='ending'>" in log, log
    assert ship.sinkings["combat"] == 1, ship.sinkings["combat"]

    captain = Captain()
    captain.fighter = 0
    captain.navigator = 100
    ship = OurShip(captain)
    ship.size = -1
    sunk, log = do_combat_encounter(ship)
    assert sunk is False, sunk
    assert "<p class='ending'>" not in log, log
    assert ship.sinkings["combat"] == 1, ship.sinkings["combat"]

    captain = Captain()
    ship = OurShip(captain)
    ship.size = 100
    sunk, log = do_combat_encounter(ship)
    assert sunk is False, sunk
    assert "<p class='ending'>" not in log, log
    assert ship.sinkings["combat"] == 1, ship.sinkings["combat"]

    # do_location
    captain = Captain()
    ship = OurShip(captain)
    destination = data.place_names[0]
    days = 0
    log = do_location(ship, destination, days, data.place_names)
    assert destination in ship.visited, (destination, ship.visited)
    assert "less than a day’s" in log, log
    assert log.startswith("<span>") and log.endswith("</span>"), log

    days = 1
    log = do_location(ship, destination, days, data.place_names)
    assert "one day’s" in log, log

    days = 2
    log = do_location(ship, destination, days, data.place_names)
    assert "two days’" in log, log

    ship.visited = set(data.place_names)
    do_location(ship, destination, days, data.place_names)
    assert ship.visited == {destination}, ship.visited
