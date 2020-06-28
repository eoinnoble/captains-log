import re


def begins_with_vowel(word: str) -> str:
    """
    Returns the correct indefinite article depending on the starting letter of the word
    """
    return "an" if word[0].lower() in "aeiou" else "a"


def get_file(file_name: str) -> list:
    """
    Takes a file name (string), reads the file line by line and saves it to a list,
    which it then returns.
    """
    with open(file_name, "r", encoding="utf-8") as my_file:
        return my_file.read().split("\n")


def get_word_count(text: str) -> int:
    """
    Returns number of words in `text` minus HTML element tags
    """
    return len(list(filter(None, re.split(r"\s+", re.sub(r"<(.*?)>+", "", text)))))


if __name__ == "__main__":
    # begins_with_vowel
    assert begins_with_vowel("Dog") == "a"
    assert begins_with_vowel("Apple") == "an"

    # get_file
    file_contents = get_file("data/wind-good.txt")
    assert len(file_contents) == 3, file_contents

    # get_word_count
    text = "<span>Hello!</span>"
    assert get_word_count(text) == 1, get_word_count(text)

    text = "<span class='something'>Hello!</span>"
    assert get_word_count(text) == 1, get_word_count(text)

    text = "<span class='something'>Hello there!</span>"
    assert get_word_count(text) == 2, get_word_count(text)
