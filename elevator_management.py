# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 12:57:19 2019

@author: PaulJ
"""

import unittest


class Dinglemouse(object):
    # The Lift never changes direction until there are no more people wanting
    # to get on/off in the direction it is already travelling

    def __init__(self, queues, capacity):
        self.UP = 1
        self.DOWN = 0
        # convert queues to lists
        self.queues = [[passenger for passenger in floor] for floor in queues]
        self.capacity = capacity
        self.levels = len(queues)
        self.top_level = self.levels - 1
        self.stops = []
        self.move_elevator(0)
        self.passengers = []
        self.curr_dir = self.UP

    def theLift(self):
        while not self.everybody_home():
            self.load_elevator()  # if elevator was prev. going in their dir.
            self.unpush_button()
            self.queue_push_buttons()
            try:
                next_floor = self.choose_stop()  # if in same dir. prev. going
            except ValueError:
                self.curr_dir = not self.curr_dir
                try:
                    self.load_elevator()  # Give them another chance to laod
                    next_floor = self.choose_stop()
                except ValueError:
                    raise ValueError("Help! I don't know where to go")
            self.move_elevator(next_floor)
            self.unload_elevator()
        return self.stops

    def everybody_home(self):
        for level_no, level_queue in enumerate(self.queues):
            for a_person in level_queue:
                if a_person != level_no:
                    return False
        if not bool(self.passengers):
            if self.curr_floor != 0:
                self.move_elevator(0)
            return True
        else:
            return False

    def queue_push_buttons(self):
        for level_no, level_queue in enumerate(self.queues):
            for a_person in level_queue:
                if a_person > level_no:
                    self.buttons_pushed[level_no][self.UP] = True
                elif a_person < level_no:
                    self.buttons_pushed[level_no][self.DOWN] = True

    def choose_stop(self):
        if self.curr_dir == self.UP:
            floor_search_range = range(self.curr_floor + 1, self.top_level + 1)
        else:
            floor_search_range = range(self.curr_floor - 1, -1, -1)
        for floor in floor_search_range:
            if floor in self.passengers:  # look for current pass dest.
                return floor
            if self.buttons_pushed[floor][self.curr_dir]:  # look for queued pa
                return floor
        if self.curr_dir == self.UP:
            floor_search_range = range(self.top_level, self.curr_floor, -1)
        else:
            floor_search_range = range(0, self.curr_floor)

        for floor in floor_search_range:  # Look for queuees for opp. direction
                if self.buttons_pushed[floor][not self.curr_dir]:
                    return floor
        raise ValueError  # no floor to choose in current direction

    def move_elevator(self, next_floor):
        self.stops.append(next_floor)
        self.curr_floor = next_floor

    def unload_elevator(self):
        if not self.passengers:
            return
        result_passengers = []
        for a_passenger in self.passengers[:]:
            if a_passenger == self.curr_floor:
                self.queues[self.curr_floor].append(a_passenger)
                self.passengers.remove(a_passenger)
            else:
                result_passengers.append(a_passenger)
        self.passengers = result_passengers[:]

    def load_elevator(self):
        this_floor_queue = self.queues[self.curr_floor][:]
        for a_queuee in this_floor_queue:
            if len(self.passengers) >= self.capacity:
                return
            if a_queuee > self.curr_floor and self.curr_dir == self.UP:
                self.passengers.append(a_queuee)
                self.queues[self.curr_floor].remove(a_queuee)
            if a_queuee < self.curr_floor and self.curr_dir == self.DOWN:
                self.passengers.append(a_queuee)
                self.queues[self.curr_floor].remove(a_queuee)

    def unpush_button(self):
        self.buttons_pushed = [  # (Down_button, Up_button)
            [False, False] for x in range(len(self.queues))]


class LiftTestMethods(unittest.TestCase):
    tests = [[((), (), (5, 5, 5), (), (), (), ()), 5,
              [0, 2, 5, 0]],
             [((), (), (1, 1), (), (), (), ()), 5,
              [0, 2, 1, 0]],
             [((), (3,), (4,), (), (5,), (), ()), 5,
              [0, 1, 2, 3, 4, 5, 0]],
             [((), (0,), (), (), (2,), (3,), ()), 5,
              [0, 5, 4, 3, 2, 1, 0]],
             [[[3], [2], [0], [2], [], [], [5]], 5,
              [0, 1, 2, 3, 6, 5, 3, 2, 0]],
             [[[], [], [4, 4, 4, 4], [], [2, 2, 2, 2], [], []], 2,
              [0, 2, 4, 2, 4, 2, 0]]]

    def test_basic(self):
        for queues, capacity, answer in self.tests:
            print('\n\n\n163:answer:', answer)
            lift = Dinglemouse(queues, capacity)
            self.assertEqual(lift.theLift(), answer)


if __name__ == '__main__':
    unittest.main()
