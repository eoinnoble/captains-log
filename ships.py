# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 09:25:05 2016

@author: enoble
"""

import random, cl_data, cl_funcs

class Ship(object):
    def __init__(self):
        self.type = random.choice(list(cl_data.ship_types.keys()))
        self.size = cl_data.ship_types[self.type]
        self.crew_health = (20 * self.size) + 40
        self.crew_sanity = (20 * self.size) + 40
        self.capacity = (20 * self.size) + 40
        self.provisions = 40 # 40 days' worth
        self.rum = 40
        self.coffers = 40
        self.name = random.choice(cl_data.ship_names)
        self.destroyed = False
        
    def __str__(self):
        self.description = "We sail on the " + self.type + " “" + self.name + "”."
        return self.description

# Need a different class for enemy vessels as they don't need names
class Enemy(object):
    def __init__(self, our_ship):
        self.type = random.choice(list(cl_data.ship_types.keys()))
        self.size = cl_data.ship_types[self.type]
        self.attacking = self.size >= our_ship.size
        self.flag = random.choice(cl_data.flags)
        self.cannon = cl_data.ship_weapons[self.size]
        self.verb = random.choice(cl_data.enemy_large_verb)
        if (self.size < our_ship.size):
            self.adj = random.choice(cl_data.enemy_small_adj)
            self.verb = random.choice(cl_data.enemy_small_verb)
        elif (self.size > our_ship.size):
            self.adj = random.choice(cl_data.enemy_large_adj)
        else:
            self.adj = random.choice(cl_data.enemy_equal_adj)
            
        self.description = ("We came across " + cl_funcs.begins_with_vowel(self.adj) + " " + self.adj + " " + 
                self.type + " with " + self.cannon + ", flying " + cl_funcs.begins_with_vowel(self.flag) + 
                " " + self.flag + " flag, " + self.verb + ".")
        
    def __str__(self):
        return self.description
            