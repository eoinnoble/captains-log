import codecs

import arrow
from bs4 import BeautifulSoup

import captains
import markup
import ships
import travel
import utils


# Python doesn't do well with dates pre-1900, so we use Arrow
START_DATE = arrow.get("1767-01-01", "YYYY-MM-DD")


def captains_log(word_count: int):
    """
    This function plays the game and outputs a log text of approximate length `word_count`
    """
    text_to_output = ""
    log_word_count = 0

    # We keep generating luckless captains until we reach {word_count} words
    while log_word_count < word_count:
        days_spent = 0
        (
            current_captain,
            current_ship,
            initial_destination,
            distance,
            current_direction,
            first_log,
        ) = travel.generate_captain()

        captain_log = markup.parchment_start
        captain_log += travel.get_date(START_DATE)
        captain_log += first_log
        captain_log += travel.run_captain(
            distance, current_ship, days_spent, START_DATE, initial_destination
        )

        log_word_count += utils.get_word_count(captain_log)
        text_to_output += captain_log

    # Print out the stats for this run
    text_to_output += (
        f"\n\n<p class='stats'>You made {captains.Captain.format_num_instances()}, and lost:</p>"
        f"{ships.OurShip.format_num_instances()}"
    )

    # Make the log valid HTML and write it to a file
    with codecs.open("output/captains-log.html", "w", "utf-8") as output:
        text_to_output = markup.doc_head + text_to_output + markup.doc_end
        soup = BeautifulSoup(text_to_output, "html.parser")
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
