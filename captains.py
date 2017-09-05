# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:50:44 2016

@author: enoble
"""

import random
import cl_data


class Captain:
    """Generate a captain with random name and attributes (ranging from 0–100)"""

    def __init__(self):
        self.name = random.choice(cl_data.captain_names)
        self.health = random.randint(0, 100)
        self.sanity = random.randint(0, 100)
        self.drunkard = random.randint(0, 100)
        self.fighter = random.randint(0, 100)
        self.navigator = random.randint(0, 100)
        self.diplomat = random.randint(0, 100)
        self.merchant = random.randint(0, 100)

    def __repr__(self):
        return ',\n'.join(sorted(['{0} => {1}'.format(key, getattr(self, key)) for key in self.__dict__]))
        

if __name__ == '__main__':
    test = Captain()
    assert len(test.name) > 0
    assert len(test.__dict__) == 8
