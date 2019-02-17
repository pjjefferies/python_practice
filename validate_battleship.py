# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:40:36 2019

@author: PaulJ
"""

# There must be single battleship (size of 4 cells), 2 cruisers (size 3),
# 3 destroyers (size 2) and 4 submarines (size 1). Any additional ships are not
# allowed, as well as missing ships.
# The ship cannot overlap or be in contact with any other ship, neither by edge
# nor by corner.
    
    from contextlib import suppress
    from copy import deepcopy
    
    
    def validate_battlefield(field):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        bf_size = len(field)
    
        # ship_board = deepcopy(field)
        bat_field_str = [''.join(map(str,row)) for row in field]
    
        bat_field_inv = deepcopy(field)
    
        for ship_len in ships:
            ship = '1' * ship_len
    
            # look for ship (group of [1 1 1 1]), false if no
            ship_found = False
    
            # Look for horizontal ship
            for row_no, row in enumerate(bat_field_str):
                with suppress(ValueError):
                    col_no = row.index(ship)
                    ship_found = True
                    break

            # Look for vertical ship
            if not ship_found:
                # Set-up inverse board
                bat_field_inv = [[bat_field_str[col_no][row_no]
                                  for col_no, _ in enumerate(bat_field_str)]
                                 for row_no, _ in enumerate(bat_field_str[0])]
                bat_field_inv_str = [''.join(map(str, row))
                                     for row in bat_field_inv]
                for row_no, row in enumerate(bat_field_inv_str):
                    with suppress(ValueError):
                        col_no = row.index(ship)
                        ship_found = True
                        bat_field_str = bat_field_inv_str
                        break
    
            if not ship_found:
                return False  # Ship not found
    
            # clear ship from field
            bat_field_str[row_no] = (bat_field_str[row_no][:col_no] +
                                     '0' * ship_len +
                                     bat_field_str[row_no][col_no + ship_len:])
    
            # Search around ship for clear space
            valid_ship_pos = not max(
                [max(map(int, bat_field_str[max(min(row_no + rel_row, bf_size-1),
                                                    0)]
                                           [max(col_no-1, 0):col_no+ship_len+1]))
                 for rel_row in range(-1, 2)])
    
            if not valid_ship_pos:
                return False
    
        # Check for unwanted shps
        unwanted_ships = max(
            [max(map(int, bat_field_str[row_no]))
             for row_no, _ in enumerate(bat_field_str)])
    
        return not unwanted_ships
