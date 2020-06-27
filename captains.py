import random

import inflect

import cl_data


class Captain:
    """
    Generate a captain with random name and attributes (ranging from 0–100)
    """

    num_instances = 0

    def __init__(self):
        self.diplomat = random.randint(0, 101)
        self.drunkard = random.randint(0, 101)
        self.fighter = random.randint(0, 101)
        self.health = random.randint(0, 101)
        self.merchant = random.randint(0, 101)
        self.name = random.choice(cl_data.captain_names)
        self.navigator = random.randint(0, 101)
        self.sanity = random.randint(0, 101)

        Captain.num_instances = Captain.num_instances + 1

    def __repr__(self) -> str:
        return ",\n".join(
            sorted([f"{key}: {getattr(self, key)}" for key in self.__dict__])
        )

    @staticmethod
    def format_num_instances() -> str:
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
    assert len(test.name) > 0, test.name
    assert len(test.__dict__) == 8, test.__dict__
    assert Captain.num_instances == 1, Captain.num_instances
    assert test.format_num_instances() == "one captain", test.format_num_instances()
    print(test)
