import random
from typing import List

import inflect

import cl_data
from cl_funcs import begins_with_vowel
from captains import Captain


# All ships have a type and a size
class Ship:
    def __init__(self):
        self.type = random.choice(list(cl_data.ship_types.keys()))
        self.size = cl_data.ship_types[self.type]


# Our hero's ship has some extra attributes
class Vessel(Ship):
    # Keep track of some stats for the end
    num_instances = 0
    sinkings = {"combat": 0, "sobriety": 0, "starvation": 0}

    def __init__(self, captain: Captain):
        Ship.__init__(self)
        self.captain = captain
        self.crew_health = (20 * self.size) + 40
        self.crew_sanity = (20 * self.size) + 40
        self.capacity = (20 * self.size) + 40
        self.provisions = 40  # 40 days' worth
        self.rum = 40
        self.name = random.choice(cl_data.ship_names)
        self.visited: List[str] = []
        Vessel.num_instances = Vessel.num_instances + 1

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

        for key, value in Vessel.sinkings.items():
            if value:
                res += f"<li>{p.number_to_words(Vessel.sinkings[key])} to {key}</li>"

        res += "</ul>"

        return res

    @staticmethod
    def sink(cause: str) -> None:
        """
        Increment the shared dict of causes of sinkings accordingly
        """
        getattr(Vessel, "sinkings")[cause] += 1


# Enemy vessels have different attributes from our hero's vessel
class Enemy(Ship):
    def __init__(self, our_ship: Vessel):
        super().__init__()
        self.attacking = self.size >= our_ship.size
        self.flag = random.choice(cl_data.flags)
        self.cannon = cl_data.ship_weapons[self.size]
        self.our_ship = our_ship

    @property
    def adj(self) -> str:
        """Return the correct adjective for this size of vessel"""
        if self.size < self.our_ship.size:
            return random.choice(cl_data.enemy_small_adj)
        elif self.size > self.our_ship.size:
            return random.choice(cl_data.enemy_large_adj)
        else:
            return random.choice(cl_data.enemy_equal_adj)

    @property
    def description(self) -> str:
        adj = self.adj
        return (
            f"We came across {begins_with_vowel(adj)} {adj} {self.type} with "
            f"{self.cannon}, flying {begins_with_vowel(self.flag)} {self.flag} flag, {self.verb}."
        )

    @property
    def verb(self) -> str:
        """Return the correct verb for this size of vessel"""
        if self.size < self.our_ship.size:
            return random.choice(cl_data.enemy_small_verb)
        else:
            return random.choice(cl_data.enemy_large_verb)

    def __str__(self) -> str:
        return self.description


if __name__ == "__main__":
    captain = Captain()
    us = Vessel(captain)
    us.size = 2
    assert us.name  # This requires that a file be accessed
    assert us.num_instances == 1
    assert us.destroyed is False
    us.crew_health = 0
    assert us.destroyed is True
    assert Vessel.sinkings["combat"] == 0
    us.sink("combat")
    assert Vessel.sinkings["combat"] == 1

    them = Enemy(us)
    assert them.flag  # This requires that a file be accessed
    them.size = 1
    assert them.adj in cl_data.enemy_small_adj
    assert them.verb in cl_data.enemy_small_verb
    them.size = 3
    assert them.adj in cl_data.enemy_large_adj
    assert them.verb in cl_data.enemy_large_verb
    them.size = 2
    assert them.adj in cl_data.enemy_equal_adj
    assert them.verb in cl_data.enemy_large_verb

    print(us)
    print(them)
