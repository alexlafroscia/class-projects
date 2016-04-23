from replacement_algorithms.base import BaseReplacement
from random import random
from math import floor


class DemoReplacement(BaseReplacement):

    """
    Demo Replacement Algorithm

    Randomly remove pages from RAM whenever necessary

    Used to make the initial setup of the simulation without worrying about
    the replacement algorithm.
    """

    name = 'Demo'

    def free_memory(self, page_table):
        """
        Test replacement algorithm

        Randomly remove something from the page table to test it out
        """
        num_frames = len(page_table.keys())
        rand = int(floor(random() * num_frames))
        key = page_table.get(rand)
        return page_table.free_indecies(key)
