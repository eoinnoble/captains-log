import random

import inflect

import cl_data


class Captain:
    """
    Generate a captain with random name and attributes (ranging from 0–100)
    """

    num_instances = 0

    def __init__(self):
        self.name = random.choice(cl_data.captain_names)
        self.health = random.randint(0, 100)
        self.sanity = random.randint(0, 100)
        self.drunkard = random.randint(0, 100)
        self.fighter = random.randint(0, 100)
        self.navigator = random.randint(0, 100)
        self.diplomat = random.randint(0, 100)
        self.merchant = random.randint(0, 100)
        Captain.num_instances = Captain.num_instances + 1

    def __repr__(self):
        return ",\n".join(
            sorted([f"{key} => {getattr(self, key)}" for key in self.__dict__])
        )

    @staticmethod
    def return_count():
        if Captain.num_instances:
            p = inflect.engine()
            return (
                f"{p.number_to_words(Captain.num_instances)} "
                f"{p.plural('captain', Captain.num_instances)}"
            )
        else:
            return ""


if __name__ == "__main__":
    test = Captain()
    assert len(test.name) > 0
    assert len(test.__dict__) == 8
