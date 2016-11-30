# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:50:44 2016

@author: enoble
"""

import random, cl_data

class Captain(object):
    
    def __init__(self):
        self.name= random.choice(cl_data.captain_names)
        self.health = random.randint(0, 100)
        self.sanity = random.randint(0, 100)
        self.drunkard = random.randint(0, 100)
        self.fighter = random.randint(0, 100)
        self.navigator = random.randint(0, 100)
        self.diplomat = random.randint(0, 100)
        self.merchant = random.randint(0, 100)