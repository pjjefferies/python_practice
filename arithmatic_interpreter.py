# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 00:17:19 2019

@author: PaulJ
"""

import unittest
import re
from contextlib import suppress


def tokenize(expression):
    if expression == "":
        return []

    regex_str = '\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*'
    regex = re.compile(regex_str)
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        try:
            equal_loc = tokens.index('=')
            if equal_loc != 1:
                raise ValueError
            identifier = tokens[0]
            assignment = True
            expression = tokens[2:]
        except ValueError:
            assignment = False
            expression = tokens[:]

        try:
            result= self.eval_exp(expression)
        except ValueError:
            raise

        if assignment:
            self.vars[identifier] = result

        return result

    def eval_exp(self, expression):
        # Look for empty express:
        if not expression:
            return ''

        # look for expressions in parenthesis
        with suppress(ValueError, AttributeError):
            first_left_paren = expression.index('(')
            open_parens_count = 1
            matching_right_paren = 0
            for a_char_no, a_char in enumerate(
                    expression[first_left_paren + 1:], first_left_paren + 1):
                open_parens_count = (open_parens_count + 1 if a_char == '('
                                     else (open_parens_count - 1
                                           if a_char == ')'
                                           else open_parens_count))
                if open_parens_count == 0:
                    matching_right_paren = a_char_no
                    break
            if not matching_right_paren:
                raise ValueError
            return self.eval_exp(
                expression[:max(first_left_paren, 0)] +
                [self.eval_exp(expression[
                    first_left_paren + 1:matching_right_paren])] +
                expression[matching_right_paren + 1:])

        # look for variables
        poss_var_locs = []
        for i, x in enumerate(expression):
            if isinstance(x, (float, int)) or x in '()*/%+-':
                continue
            try:
                float(x)
                continue
            except ValueError:
                poss_var_locs.append(i)
        poss_vars = [expression[x] for x in poss_var_locs]
        for a_var_loc_no, _ in enumerate(poss_var_locs):
            try:
                expression[poss_var_locs[a_var_loc_no]] = (
                    self.vars[poss_vars[a_var_loc_no]])
            except KeyError:
                raise ValueError

        # look for only a number
        if len(expression) == 1:
            with suppress(ValueError):
                return_val = float(expression[0])
                if return_val == int(return_val):
                    return int(return_val)
                else:
                    return return_val

        # look for first of *, /, %
        multiplicative = [i for i, x in enumerate(expression)
                          if str(x) in '*/%']
        if multiplicative:
            first_mult = multiplicative[0]
            if first_mult == 0 or first_mult == (len(expression) - 1):
                raise ValueError
            operator = expression[first_mult]
            expr1 = self.eval_exp([expression[first_mult - 1]])
            expr2 = self.eval_exp([expression[first_mult + 1]])
            multiplicative_result = (
                expr1 * expr2 if operator == '*'
                else (expr1 % expr2 if operator == '%'
                      else (expr1/expr2 if (expr1/expr2 != int(expr1/expr2))
                            else int(expr1/expr2))))
            return self.eval_exp(expression[:first_mult - 1] +
                                 [multiplicative_result] +
                                 expression[first_mult + 2:])

        # look for first of +, -
        additive = [i for i, x in enumerate(expression)
                    if str(x) in '+-']
        if additive:
            first_add = additive[0]
            if first_add == 0 or first_add == (len(expression) - 1):
                raise ValueError
            operator = expression[first_add]
            expr1 = self.eval_exp(expression[first_add - 1:first_add])
            expr2 = self.eval_exp(expression[first_add + 1:first_add + 2])
            additive_result = (expr1 + expr2 if operator == '+'
                               else expr1 - expr2)
            return self.eval_exp(expression[:first_add - 1] +
                                 [additive_result] +
                                 expression[first_add + 2:])

        raise ValueError




class InterpreterTestMethods(unittest.TestCase):
    tests = [['1 + 1', 2],
             ['2 - 1', 1],
             ['2 * 3', 6],
             ['8 / 4', 2],
             ['7 % 4', 3],
             ['x = 1', 1],
             ['x', 1],
             ['x + 3', 4],
             ['y', ValueError],
             ['4 + 2 * 3', 10],
             ['4 / 2 * 3', 6],
             ['7 % 2 * 8', 8],
             ['(7 + 3) / (2 * 2 + 1)', 2]]

    def test_basic(self):
        interpreter = Interpreter()
        for expression, answer in self.tests:
            print('\n')
            try:
                result = interpreter.input(expression)
            except ValueError:
                result = ValueError
            print('expression:', expression, ', answer:', answer,
                  ', result:', result)
            self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()
