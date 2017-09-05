# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 09:25:05 2016

@author: enoble
"""

import random

import cl_data
import cl_funcs


# All ships have a type and a size
class Ship:

    def __init__(self):
        self.type = random.choice(list(cl_data.ship_types.keys()))
        self.size = cl_data.ship_types[self.type]


# Our hero's ship has some extra attributes
class Vessel(Ship):

    def __init__(self):
        Ship.__init__(self)
        self.crew_health = (20 * self.size) + 40
        self.crew_sanity = (20 * self.size) + 40
        self.capacity = (20 * self.size) + 40
        self.provisions = 40  # 40 days' worth
        self.rum = 40
        self.coffers = 40
        self.name = random.choice(cl_data.ship_names)
        self.destroyed = False

    def __str__(self):
        self.description = 'We sail on the ' + self.type + ' “' + self.name + '”.'
        return self.description


# Enemy vessels have different attribute from our hero's vessel
class Enemy(Ship):

    def __init__(self, our_ship):
        Ship.__init__(self)
        self.attacking = self.size >= our_ship.size
        self.flag = random.choice(cl_data.flags)
        self.cannon = cl_data.ship_weapons[self.size]
        self.verb = random.choice(cl_data.enemy_large_verb)
        if self.size < our_ship.size:
            self.adj = random.choice(cl_data.enemy_small_adj)
            self.verb = random.choice(cl_data.enemy_small_verb)
        elif self.size > our_ship.size:
            self.adj = random.choice(cl_data.enemy_large_adj)
        else:
            self.adj = random.choice(cl_data.enemy_equal_adj)
            
        self.description = ('We came across ' + cl_funcs.begins_with_vowel(self.adj) + ' ' + self.adj + ' ' +
                            self.type + ' with ' + self.cannon + ', flying ' + cl_funcs.begins_with_vowel(self.flag) +
                            ' ' + self.flag + ' flag, ' + self.verb + '.')
        
    def __str__(self):
        return self.description


if __name__ == '__main__':
    us = Vessel()
    them = Enemy(us)
    assert us.name and them.flag  # These require files to be accessed
    print(us, them)
