import random
from typing import Set

import inflect

import data
from captains import Captain
from utils import begins_with_vowel


# All ships have a type and a size
class BaseShip:
    def __init__(self):
        self.type = random.choice(list(data.ship_types.keys()))
        self.size = data.ship_types[self.type]


class OurShip(BaseShip):
    # Keep track of some stats for the end
    num_instances = 0
    sinkings = {"combat": 0, "sobriety": 0, "starvation": 0}

    def __init__(self, captain: Captain):
        super().__init__()
        self.captain = captain
        self.crew_health = (20 * self.size) + 40
        self.crew_sanity = (20 * self.size) + 40
        self.capacity = (20 * self.size) + 40
        self.provisions = 40  # 40 days' worth
        self.rum = 40
        self.name = random.choice(data.ship_names)
        self.visited: Set[str] = set()
        OurShip.num_instances = OurShip.num_instances + 1

    def __str__(self) -> str:
        return self.description

    @property
    def description(self):
        return f"We sail on the {self.type} “{self.name}”."

    @property
    def destroyed(self) -> bool:
        return self.crew_health <= 0 or self.crew_sanity <= 0

    @staticmethod
    def format_num_instances() -> str:
        """
        Format the record of all sinkings for inclusion in our log output
        """
        p = inflect.engine()
        res = "\n<ul class='stats'>"

        for key, value in OurShip.sinkings.items():
            if value:
                res += f"<li>{p.number_to_words(OurShip.sinkings[key])} to {key}</li>"

        res += "</ul>"

        return res

    @staticmethod
    def sink(cause: str) -> None:
        """
        Increment the shared dict of causes of sinkings accordingly
        """
        getattr(OurShip, "sinkings")[cause] += 1


class EnemyShip(BaseShip):
    def __init__(self, our_ship: OurShip):
        super().__init__()
        self.attacking = self.size >= our_ship.size
        self.flag = random.choice(data.flags)
        self.cannon = data.ship_weapons[self.size]
        self.our_ship = our_ship

    @property
    def adj(self) -> str:
        """Return the correct adjective for this size of OurShip"""
        if self.size < self.our_ship.size:
            return random.choice(data.enemy_small_adj)
        elif self.size > self.our_ship.size:
            return random.choice(data.enemy_large_adj)
        else:
            return random.choice(data.enemy_equal_adj)

    @property
    def description(self) -> str:
        adj = self.adj
        return (
            f"We came across {begins_with_vowel(adj)} {adj} {self.type} with "
            f"{self.cannon}, flying {begins_with_vowel(self.flag)} {self.flag} flag, {self.verb}."
        )

    @property
    def verb(self) -> str:
        """Return the correct verb for this size of OurShip"""
        if self.size < self.our_ship.size:
            return random.choice(data.enemy_small_verb)
        else:
            return random.choice(data.enemy_large_verb)

    def __str__(self) -> str:
        return self.description


if __name__ == "__main__":
    captain = Captain()
    us = OurShip(captain)
    us.size = 2
    assert us.name  # This requires that a file be accessed
    assert us.num_instances == 1
    assert us.destroyed is False
    us.crew_health = 0
    assert us.destroyed is True
    assert OurShip.sinkings["combat"] == 0
    us.sink("combat")
    assert OurShip.sinkings["combat"] == 1

    them = EnemyShip(us)
    assert them.flag  # This requires that a file be accessed
    them.size = 1
    assert them.adj in data.enemy_small_adj
    assert them.verb in data.enemy_small_verb
    them.size = 3
    assert them.adj in data.enemy_large_adj
    assert them.verb in data.enemy_large_verb
    them.size = 2
    assert them.adj in data.enemy_equal_adj
    assert them.verb in data.enemy_large_verb

    print(us)
    print(them)
