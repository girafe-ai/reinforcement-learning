from __future__ import print_function

import gymnasium as gym
from gymnasium import spaces
from gymnasium.utils import seeding

import numpy as np

import itertools
import logging
from six import StringIO
import sys

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

class IllegalMove(Exception):
    pass

class Game2048Env(gym.Env):
    def __init__(
        self, 
        render_mode: str = "ansi", 
        seed: int | None = None,
        illegal_move_reward: float = 0.0,
        max_tile: int = 2048
    ):
        self.render_mode = render_mode
        self.size = 4
        self.w = self.size
        self.h = self.size

        self.score = 0 # this score may be differ from the reward function!

        # self.action_space = spaces.Discrete(...)
        # self.observation_space = spaces.Box(...)
        
        self.set_illegal_move_reward(illegal_move_reward, max_tile)
        self.set_max_tile(max_tile)

        self.seed(seed)
        self.reset()

    def seed(self, seed: int | None = None) -> int:
        self.np_random, seed = seeding.np_random(seed)
        return seed

    def set_illegal_move_reward(self, reward, max_tile):
        """ Define the penalty for performing an illegal move """

        self.illegal_move_reward = reward
        self.reward_range = (self.illegal_move_reward, float(max_tile))

    def set_max_tile(self, max_tile):
        """Define the maximum tile that will end the game (e.g. 2048). None means no limit.
           This does not affect the state returned."""
        assert max_tile is None or isinstance(max_tile, int)
        self.max_tile = max_tile

    # Implement gym interface
    def step(self, action):
        """Perform one step of the game. This involves moving and adding a new tile."""
        logging.debug("Action {}".format(action))
        score = 0
        done = None
        info = {
            'illegal_move': False,
        }
        try:
            # YOUR CODE GOES HERE
            pass
        except IllegalMove:
            logging.debug("Illegal move")
            info['illegal_move'] = True
            done = True
            reward = self.illegal_move_reward

        info['highest'] = self.highest()

        # Return observation (board state), reward, done, truncated and info dict
        return np.stack(self.matrix), reward, done, done, info

    def reset(self):
        self.matrix = np.zeros((self.h, self.w), int)
        self.score = 0

        logging.debug("Adding tiles")
        self.add_tile()
        self.add_tile()

        return np.stack(self.matrix)

    def render(self):
        mode = self.render_mode
        assert mode in ['ansi']
        outfile = StringIO()
        s = 'Score: {}\n'.format(self.score)
        s += 'Highest: {}\n'.format(self.highest())

        npa = np.array(self.matrix)
        grid = npa.reshape((self.size, self.size))
        s += "{}\n".format(grid)
        outfile.write(s)
        return outfile.getvalue()

    # Implement 2048 game
    def add_tile(self):
        """Add a tile, probably a 2 but maybe a 4"""
        possible_tiles = np.array([2, 4])
        tile_probabilities = np.array([0.9, 0.1])
        # YOUR CODE GOES HERE

    def get(self, x, y):
        """Return the value of one square."""
        return self.matrix[x, y]

    def set(self, x, y, val):
        """Set the value of one square."""
        self.matrix[x, y] = val

    def empties(self):
        """Return a 2d numpy array with the location of empty squares."""
        return np.argwhere(self.matrix == 0)

    def highest(self):
        """Report the highest tile on the board."""
        return np.max(self.matrix)

    def move(self, direction, trial=False):
        """Perform one move of the game. Shift things to one side then,
        combine. directions 0, 1, 2, 3 are up, right, down, left.
        Returns the score that [would have] got."""
        if not trial:
            if direction == 0:
                logging.debug("Up")
            elif direction == 1:
                logging.debug("Right")
            elif direction == 2:
                logging.debug("Down")
            elif direction == 3:
                logging.debug("Left")

        changed = False
        move_score = 0
        # YOUR CODE GOES HERE

    def combine(self, shifted_row):
        """Combine same tiles when moving to one side. This function always
           shifts towards the left. Also count the score of combined tiles."""
        move_score = 0
        combined_row = [0] * self.size
        skip = False
        output_index = 0
        for p in pairwise(shifted_row):
            # YOUR CODE GOES HERE
            pass

    def shift(self, row, direction):
        """Shift one row left (direction == 0) or right (direction == 1), combining if required."""
        length = len(row)
        assert length == self.size
        assert direction == 0 or direction == 1

        # Shift all non-zero digits up
        shifted_row = [i for i in row if i != 0]

        # Reverse list to handle shifting to the right
        if direction:
            shifted_row.reverse()

        (combined_row, move_score) = self.combine(shifted_row)

        # Reverse list to handle shifting to the right
        if direction:
            combined_row.reverse()

        assert len(combined_row) == self.size
        return (combined_row, move_score)

    def isend(self):
        """ Clarify whether game ended or not """

        if self.max_tile is not None and self.highest() == self.max_tile:
            return True

        for direction in range(4):
            try:
                self.move(direction, trial=True)
                # Not the end if we can do any move
                return False
            except IllegalMove:
                pass
        return True

    def get_board(self) -> np.ndarray:
        """ Retrieve the whole board, useful for testing """
        return self.matrix

    def set_board(self, new_board) -> np.ndarray:
        """ Retrieve the whole board, useful for testing """
        self.matrix = new_board