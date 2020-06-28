import codecs
import textwrap

import arrow
from bs4 import BeautifulSoup

import captains
import data
import navigation
import ships
import travel
import utils


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
        CAPTAIN_TEXT += PARCHMENT_START + travel.get_date(current_date)

        # Initialise objects and places
        (
            current_captain,
            current_ship,
            current_location,
            current_destination,
            distance,
            current_direction,
            first_log,
        ) = travel.start()

        CAPTAIN_TEXT += first_log
        days_completed = 0

        # We keep travelling until we are destroyed
        while not current_ship.destroyed:

            date_already_logged = False

            # We keep travelling towards the destination until we reach it
            while distance > 0:

                # We keep track of the day's entry in case there's nothing interesting
                # to commit to the main log
                day_log_entry = "<span>"

                sunk, provision_log = travel.handle_provisions(current_ship)
                day_log_entry += provision_log
                if sunk:
                    CAPTAIN_TEXT += day_log_entry
                    break

                sunk, encounter_log = travel.do_encounter(current_ship)
                day_log_entry += encounter_log
                if sunk:
                    CAPTAIN_TEXT += day_log_entry
                    break

                # If we have survived the encounter deck we calculate the wind
                wind = navigation.check_wind(current_captain)
                distance_travelled = 125 * wind[0]
                days_completed += 1
                current_date = current_date.shift(days=+1)
                distance -= distance_travelled

                # Check if anything interesting happened and add it to the main log if so
                if not day_log_entry == "<span>":
                    CAPTAIN_TEXT += f"\n{travel.get_date(current_date)}"
                    CAPTAIN_TEXT += f"{day_log_entry}</span>"
                    date_already_logged = True

            # If the distance is less than or equal to zero, we have arrived!
            if current_ship.destroyed:
                break

            if not date_already_logged:
                CAPTAIN_TEXT += f"\n{travel.get_date(current_date)}"
                date_already_logged = True

            CAPTAIN_TEXT += travel.do_location(
                current_ship, current_destination, days_completed, data.place_names,
            )

            (
                new_destination,
                new_distance,
                destination_log,
            ) = navigation.get_new_heading(
                current_destination, data.place_coords, current_ship.visited,
            )
            CAPTAIN_TEXT += destination_log
            current_date = current_date.shift(days=+1)

            # Re-initialise variables
            days_completed = 0
            current_destination = new_destination
            distance = new_distance
            date_already_logged = False

        log_word_count += utils.get_word_count(CAPTAIN_TEXT)
        TEXT_TO_BE_LOGGED += CAPTAIN_TEXT

    # Print out the stats for this run
    TEXT_TO_BE_LOGGED += (
        f"\n\n<p class='stats'>You made {captains.Captain.format_num_instances()}, and lost:</p>"
        f"{ships.OurShip.format_num_instances()}"
    )

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
