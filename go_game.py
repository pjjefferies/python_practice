# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:39:34 2019

@author: PaulJ
"""

import unittest
import numpy as np


class Go():
    def __init__(self, height=False, width=False):
        try:
            if not height or int(height) != height:
                raise ValueError('Height must be supplied as an integer')
            if width:
                try:
                    if int(width) != width:
                        raise ValueError(
                            'If supplied, width must be an integer')
                except ValueError:
                    raise ValueError('If supplied, width must be an integer')
        except ValueError:
            raise ValueError('Height must be supplied as an integer')
        if height < 1 or height > 25:
            raise ValueError('Height and Width must be 25 or less')
        self.height = height
        if width:
            if width < 1 or width > 25:
                raise ValueError('Height and Width must be 25 or less')
            self.width = width
        else:
            self.width = height
        self.boards = [np.full((self.height, self.width), '.')]
        self.blacks_turn = True

    def board(self):
        # return str(self)  # this is what decription wants but not tests
        return self.boards[-1].tolist()

    def move(self, *move_str):
        # print('move_str:', move_str, ', len(move_str):', len(move_str))
        if len(move_str) > 1:
            for a_move_str in move_str:
                try:
                    self.move(a_move_str)
                except ValueError as e:
                    raise ValueError(e)
            return

        try:
            move_xy = self._board_pos(move_str)
            move_yz = move_xy[::-1]
        except (ValueError, IndexError):
            raise ValueError(move_str + ' is not a valid move')

        # Check if space unoccupied
        try:
            if self.boards[-1][move_yz] != '.':
                raise ValueError(move_str + ' is not empty')
        except (ValueError, IndexError):
            raise ValueError(move_str + ' is not a valid move')

        # Add stone, creating new board
        self._add_stones(move_xy, new_board=True)

        # Detect Captured stones of opposite color
        captured_stones = (
            self._detect_captured_stones(black=not self.blacks_turn))

        # Remove opposite color's captureed stones
        if captured_stones:
            self._remove_captured_stones(captured_stones)

        # Detect Captured stones of own color
        captured_stones = (
            self._detect_captured_stones(black=self.blacks_turn))

        # Check if originally placed stone is captured
        if move_xy in captured_stones:
            raise ValueError('Move ' + move_str + ' is self-capturing')

        # Remove own color stones
        if captured_stones:
            self._remove_captured_stones(captured_stones)

        # Switch Player's turn
        self._switch_player()

    def _switch_player(self):
        self.blacks_turn = not self.blacks_turn

    def handicap_stones(self, no_hc_stones):
        try:
            int(no_hc_stones)
        except ValueError:
            raise ValueError('Number of handicap stones must be an integer')
        if not ((self.width == 9 and self.width == 9) or
                (self.width == 13 and self.width == 13) or
                (self.width == 19 and self.width == 19)):
            raise ValueError(
                'Only 9x9, 13x13 and 19x19 games can be handicapped')
        if len(self.boards) > 1:
            raise ValueError(
                'Handicapping only allowed before the first move')
        if ((self.width == 9 and (no_hc_stones < 1 or no_hc_stones > 5)) or
            (self.width == 13 and (no_hc_stones < 1 or no_hc_stones > 9)) or
                (self.width == 19 and (no_hc_stones < 1 or no_hc_stones > 9))):
            raise ValueError('Number of handicap stones must be 1-5 for 9x9' +
                             ' board and 1-9 for 13x13 and 19x19 boards')
        if self.width == 9:
            self._add_stones(
                [(6, 2), (2, 6), (6, 6), (2, 2), (4, 4)][:no_hc_stones],
                new_board=True)
        elif self.width == 13:
            self._add_stones(
                [(9, 3), (3, 9), (9, 9), (3, 3), (6, 6),
                 (3, 6), (9, 6), (6, 3), (6, 9)][:no_hc_stones],
                new_board=True)
        elif self.width == 13:
            self._add_stones(
                [(15, 3), (3, 15), (15, 15), (3, 3), (9, 9),
                 (3, 9), (15, 9), (9, 3), (9, 15)][:no_hc_stones],
                new_board=True)
        else:
            raise ValueError('We have a problem')

    def size(self):
        return {'height': self.height,
                'width': self.width}

    def rollback(self, no_steps=None):
        if no_steps is None:
            raise ValueError('Number of steps to roll back must be supplied')
        elif not isinstance(no_steps, int):
            raise ValueError('Number of steps to roll back must be an integer')
        elif no_steps > (len(self.boards) - 1):
            raise ValueError('Number of roll back steps, ' + str(no_steps) +
                             ', cannot be larger than the number of steps ' +
                             'taken so far, ' + str(len(self.boards)-1))
        self.boards = self.boards[:-no_steps]
        if no_steps % 2:
            self._switch_player()

    def get_position(self, pos_str):
        try:
            pos_xy = self._board_pos(pos_str)  # (x, y)
            pos_yx = pos_xy[::-1]
        except ValueError as e:
            raise ValueError(e)
        try:
            return self.boards[-1][pos_yx]
        except IndexError:
            raise ValueError('Positions must be on board')

    def turn(self):
        return 'black' if self.blacks_turn else 'white'

    def pass_turn(self):
        self._switch_player()

    def _add_stones(self, stone_positions, new_board=True):
        if not isinstance(stone_positions, list):
            stone_positions = list(stone_positions)
        if new_board:
            temp_board = self.boards[-1]
        else:
            temp_board = self.boards.pop()
        stone_color = 'x' if self.blacks_turn else 'o'
        for stone_pos in stone_positions:
            try:
                x, y = stone_pos
                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    raise ValueError('_add stone pos. not valid')
                temp_board[y, x] = stone_color
            except ValueError:
                raise ValueError('Unable to manually add stones')
        self.boards.append(temp_board)

    def _board_pos(self, board_pos_str):
        if not (board_pos_str is isinstance(str)):
            raise ValueError('Board Position must be supplied')
        try:
            row_str = board_pos_str[:-1]
            col_str = board_pos_str[-1]
            row = self.height - int(row_str)
            col = 'ABCDEFGHJKLMONPQRSTUVWXYZ'.index(col_str)
            return (col, row)  # (x, y)
        except ValueError:
            raise ValueError('Board Position must be of form "A1"')

    def _detect_captured_stones(self, black=True):
        stone_color = 'x' if black else 'o'
        temp_board = self.boards[-1]
        stone_locs = np.where(temp_board == stone_color)
        all_stones = list(zip(list(stone_locs[1]),
                              list(stone_locs[0])))  # x, y
        captured_stones = []
        while all_stones:
            stone_xy = all_stones.pop(0)  # next stone creates start of new gro
            new_group = [stone_xy]
            new_group_search = [stone_xy]
            group_liberties = False
            while new_group_search:
                stone_xy = new_group_search.pop(0)
                stone_yx = stone_xy[::-1]
                for direct in ((-1, 0), (0, 1), (1, 0), (0, -1)):  # y, x
                    test_pos = stone_yx[0] + direct[0], stone_yx[1] + direct[1]
                    if temp_board[test_pos] == stone_color:
                        if test_pos not in new_group:
                            new_group.append(test_pos[::-1])  # x, y
                            new_group_search.append(test_pos[::-1])  # x, y
                            all_stones.remove(test_pos[::-1])  # x, y
                    if temp_board[test_pos] == '.':
                        group_liberties = True
            if not group_liberties:
                captured_stones = captured_stones + new_group
        return captured_stones

    def _remove_captured_stones(self, stones):
        """
        Remove supplied stones. stones parameter can be a tuple for one stone
        or a list of lists or tuples for multiple stones. Stones are supplied
        as (x, y)
        """
        if not isinstance(stones, list):
            stones = list(stones)
        temp_board = self.boards.pop()
        for stone_xy in stones:
            stone_yx = stone_xy[::-1]
            if temp_board[stone_yx] == '.':
                raise ValueError('Cannot remove a stone that is not there')
            temp_board[stone_yx] = '.'
        self.board.append(temp_board)

    def __str__(self):
        return '\n'.join([''.join([ele for ele in row])
                          for row in self.boards[-1]])


class TestMethods(unittest.TestCase):

    # tests = {1: [(9, 16), lambda: game.size(), ]}

    def test_basic(self):
        # Test 1
        print('\nTest 1: ', end='')
        game = Go(9)
        board = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.']]
        result = game.board()
        answer = board
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(game.board(), board)

        # Test 2
        print('\nTest 2: ', end='')
        game = Go(13)
        board = [['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.']]
        result = game.board()
        answer = board
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(game.board(), board)

        # Test 3
        print('\nTest 3: ', end='')
        game = Go(19)
        board = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.'],
                 ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                  '.', '.', '.', '.', '.', '.', '.']]
        result = game.board()
        answer = board
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(game.board(), board)

        # Test 4
        print('\nTest 4: ', end='')
        try:
            Go(32)
            print('wrong: Go(32) should throw an error')
        except ValueError:
            print('correct!')
        self.assertError(Go(32))

        # Test 5A - Placing Stones
        print('\nTest 5A: ', end='')
        game = Go(9)
        game.move('3D')
        result = game.get_position('3D')
        answer = 'x'
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)

        # Test 5B - Placing Stones
        print('\nTest 5B: ', end='')
        game.move('4D')
        result = game.get_position('4D')
        answer = 'o'
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)

        # Test 5C - Placing Stones
        print('\nTest 5C: ', end='')
        game.move('4A', '5A', '6A')
        result1 = game.get_position('4A')
        answer1 = 'x'
        result2 = game.get_position('45')
        answer2 = '0'
        result3 = game.get_position('6A')
        answer3 = 'x'
        if result1 != answer1:
            print('wrong: result1:',
                  result1, ' should be  answer1:', answer1)
        else:
            print('-1 correct!')
        self.assertEqual(result1, answer1)
        if result2 != answer2:
            print('wrong: result2:',
                  result2, ' should be  answer2:', answer2)
        else:
            print('-2 correct!')
        self.assertEqual(result2, answer2)
        if result3 != answer3:
            print('wrong: result3:',
                  result3, ' should be  answer3:', answer3)
        else:
            print('-3 correct!')
        self.assertEqual(result3, answer3)

        # Test 6A - Cannot place a stone on an existing stone
        print('\nTest 6A: ', end='')
        try:
            game.move('3D')
            print('wrong: game.move("3D") should not be allowed on existing',
                  'stone')
        except ValueError:
            print('correct!')
        self.assertError(game.move('3D'))

        # Test 6B - Cannot place a stone on an existing stone
        print('\nTest 6B: ', end='')
        try:
            game.move('4D')
            print('wrong: game.move("4D") should not be allowed on existing',
                  'stone')
        except ValueError:
            print('correct!')
        self.assertError(game.move('4D'))

        # Test 7A - Cannot place a stone out of bounds
        print('\nTest 7A: ', end='')
        try:
            game.move('3Z')
            print('wrong: game.move("3Z") should not be allowed out of bounds')
        except ValueError:
            print('correct!')
        self.assertError(game.move('3Z'))

        # Test 7B - Cannot place a stone with invalid coords.
        print('\nTest 7B: ', end='')
        try:
            game.move('66')
            print('wrong: game.move("66") should not be allowed as invalide',
                  'coords.')
        except ValueError:
            print('correct!')
        self.assertError(game.move('66'))

        # Test 8A - Capturing
        print('\nTest 8A: ', end='')
        game = Go(9)
        moves = ['4D', '3D', '4H', '5D', '3H', '4C', '5B', '4E']
        game.move(*moves)
        result = game.get_position('4D')
        answer = '.'
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result == answer)

        # Test 8B - Capturing multiple stones
        print('\nTest 8B: ', end='')
        game = Go(9)
        moves = ['6D', '7E', '6E', '6F', '4D', '5E', '5D', '7D',
                 '5C', '6C', '7H', '3D', '4E', '4F', '3E', '2E',
                 '3F', '3G', '2F', '1F', '2G', '2H', '1G', '1H',
                 '4C', '3C', '6H', '4B', '5H', '5B']
        game.move(*moves)
        captured = ['6D', '6E', '4D', '5D', '5C', '4E', '3E',
                    '3F', '2F', '2G', '1G', '4C']
        result = all([game.get_position(x) == '.' for x in captured])
        answer = True
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result == answer)

        # Test 8C - Corner Capture
        print('\nTest 8C: ', end='')
        game = Go(9)
        moves = ['9A', '8A', '8B', '9B']
        game.moves(*moves)
        result = game.get_position('9A')
        answer = '.'
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result == answer)

        # Test 8D - Multiple Captures
        print('\nTest 8D: ', end='')
        game = Go(9)
        moves = ['5D', '5E', '4E', '6E', '7D', '4F', '7E', '3E', '5F', '4D',
                 '6F', '6D', '6C', '7F', '4E', '5E']
        game.moves(*moves)
        captured = ['4E', '6D', '6E']
        result = all([game.get_position(x) == '.' for x in captured])
        answer = True
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result == answer)

        # Test 8E - Snapback
        print('\nTest 8E: ', end='')
        game = Go(9)
        moves = ['5A', '1E', '5B', '2D', '5C', '2C', '3A',
                 '1C', '2A', '3D', '2B', '3E', '4D', '4B',
                 '4E', '4A', '3C', '3B', '1A', '4C', '3C']
        game.moves(*moves)
        captured = ['4A', '4B', '4C', '3B']
        result = all([game.get_position(x) == '.' for x in captured])
        answer = True
        if result != answer:
            print('wrong: result:',
                  result, ' should be  answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result == answer)

        # Test 9 - Self-capturing throws an error
        print('\nTest 9: ', end='')
        game = Go(9)
        moves = ['4H', '8A', '8B', '9B', '9A']
        try:
            game.moves(*moves)
            print('wrong: self-capturing should throw an error')
        except ValueError:
            print('correct!')
        self.assertError(game.moves(*moves))

        # Test 10 - KO Rule
        print('\nTest 10: ', end='')
        game = Go(9)
        moves = ['5C', '5B', '4D', '4A', '3C', '3B',
                 '2D', '2C', '4B', '4C', '4B']
        try:
            game.moves(*moves)
            print('wrong: Illegal KO by white should throw an error')
        except ValueError:
            print('correct!')
        game.move('2B')
        result1 = game.get_position('2B')
        result2 = game.get_position('4B')
        answer1 = 'x'
        answer2 = '.'
        if result1 != answer1 or result2 != answer2:
            print('wrong: result1:', result1, 'should be answer1:', answer1,
                  'and result2:', result2, 'should be answer2:', answer2)
        else:
            print('correct!')
        self.assertEqual(result1, answer1)
        self.assertEqual(result2, answer2)

        # Test 11 - Handicap Stones
        print('\nTest 11: ', end='')
        game = Go(9)
        game.handicap_stones(3)
        answer = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', 'x', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', 'x', '.', '.', '.', 'x', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.']]
        result = game.board()
        if result != answer:
            print('wrong: result:', result, 'should be answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)

        # Test 12 - Board size
        print('\nTest 12: ', end='')
        game = Go(9, 16)
        answer = {'height': 9, 'width': 16}
        result = game.size()
        if result != answer:
            print('wrong: result:', result, 'should be answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)

        # Test 13 - Can get color of current turn
        print('\nTest 13: ', end='')
        game = Go(9)
        game.move('3B')
        result1 = game.turn()
        game.move('4B')
        result2 = game.turn()
        answer1 = 'white'
        answer2 = 'black'
        if result1 != answer1 or result2 != answer2:
            print('wrong: result1:', result1, 'should be answer1:', answer1,
                  'and result2:', result2, 'should be answer2:', answer2)
        else:
            print('correct!')
        self.assertEqual(result1, answer1)
        self.assertEqual(result2, answer2)

        # Test 14 - Can rollbakc a set number of turns
        print('\nTest 14: ', end='')
        game = Go(9)
        game.move('3B', '2B', '1B')
        game.rollback(3)
        result = game.board()
        answer = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.']]
        if result != answer:
            print('wrong: result:', result, 'should be answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)

        # Test 15 - Can pass turn
        print('\nTest 15: ', end='')
        game = Go(9)
        game.pass_turn()
        result = game.turn()
        answer = 'white'
        if result != answer:
            print('wrong: result:', result, 'should be answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)

        # Test 16 - Can reset the board
        print('\nTest 16: ', end='')
        game = Go(9)
        game.move('3B', '2B', '1B')
        game.reset()
        result = game.board()
        answer = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.']]
        if result != answer:
            print('wrong: result:', result, 'should be answer:', answer)
        else:
            print('correct!')
        self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()

"""
Result:

"""
