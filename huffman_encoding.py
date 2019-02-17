# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:10:34 2019

@author: PaulJ
"""

# import unittest


# takes: str; returns: [ (str, int) ] (Strings in return value are single
# characters)
def frequencies(s):
    return [(char, s.count(char)) for char in set(s)]


# takes: [ (str, int) ], str; returns: String (with "0" and "1")
def encode(freqs, s):
    if len(freqs) <= 1:
        return None
    if not s:
        return ''

    nodes_in_tree, root_node_key = create_node_tree(freqs)

    result = ''
    for a_char in s:
        curr_node = nodes_in_tree[root_node_key]
        while True:
            new_char = True
            for a_child_no in ['0', '1']:
                a_child_node = 'child_' + a_child_no
                if curr_node[a_child_node] is not None:
                    if a_char in curr_node[a_child_node]:
                        result += a_child_no
                        curr_node = nodes_in_tree[curr_node[a_child_node]]
                        new_char = False
                        continue
            if not new_char:
                continue
            break

    return result


def create_node_tree(freqs):
    nodes_to_add = {}
    for a_char, a_freq in freqs:  # adding parent, lh_child, rh_child nodes
        nodes_to_add[a_char] = {
                                'freq': a_freq,
                                'parent': None,
                                'child_0': None,
                                'child_1': None
                                }  # adding l/r_child
    nodes_in_tree = {}

    while nodes_to_add:
        node_freq = zip(nodes_to_add.keys(), [nodes_to_add[x]['freq']
                        for x in nodes_to_add])
        min_key1 = min(node_freq, key=lambda x: x[1])[0]
        node1_to_add = nodes_to_add.pop(min_key1)
        node_freq = zip(nodes_to_add.keys(), [nodes_to_add[x]['freq']
                        for x in nodes_to_add])
        min_key2 = min(node_freq, key=lambda x: x[1])[0]
        node2_to_add = nodes_to_add.pop(min_key2)

        new_node = {  # node1_to_add[0] + node2_to_add[0],
                    'freq': node1_to_add['freq'] + node2_to_add['freq'],
                    'parent': None,
                    'child_0': min_key2,
                    'child_1': min_key1}
        node1_to_add['parent'] = min_key1 + min_key2
        node2_to_add['parent'] = min_key1 + min_key2
        nodes_in_tree[min_key1] = node1_to_add
        nodes_in_tree[min_key2] = node2_to_add
        nodes_to_add[min_key1 + min_key2] = new_node
        if len(nodes_to_add) == 1:
            root_node_key = min_key1 + min_key2
            root_node = nodes_to_add.pop(root_node_key)
            nodes_in_tree[root_node_key] = root_node
    return nodes_in_tree, root_node_key


# takes [ [str, int] ], str (with "0" and "1"); returns: str
# e.g. freqs = [['b', 1], ['c', 2], ['a', 4]]
#      bits = '0000111010'
def decode(freqs, bits):
    if len(freqs) <= 1:
        return None
    if len(bits) == 0:
        return ''

    nodes_in_tree, root_node_key = create_node_tree(freqs)

    bits_list = bits[:]
    result = ''
    curr_node_key = root_node_key
    while bits_list:
        curr_node = nodes_in_tree[curr_node_key]
        curr_bit = bits_list[0]
        bits_list = bits_list[1:]

        child_str = 'child_' + curr_bit
        if nodes_in_tree[curr_node[child_str]][child_str] is None:
            result += curr_node[child_str]  # take letter
            curr_node_key = root_node_key
        else:
            curr_node_key = curr_node[child_str]  # no letter found yet, g-down

    return result



s = 'aaaabcc'
fs = frequencies(s)
encoded = encode(fs, s)
decoded = decode(fs, encoded)
print('s:', s, ', fs:', fs, ', encoded:', encoded, ', decoded:', decoded)

fs1 = [('a', 1), ('b', 1)]
test1 = ["a", "b"]
for a_test in test1:
    encoded = encode(fs1, a_test)
    decoded = decode(fs1, encoded)
    print('a_test:', a_test, ', fs1:', fs1, ', encoded:', encoded,
          ', decoded:', decoded)


"""
class InterpreterTestMethods(unittest.TestCase):
    len_tests = [["aaaabcc", 10]]  #,
"""

"""
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
"""
"""
if __name__ == '__main__':
    unittest.main()




test.describe("basic tests")
fs = frequencies("aaaabcc")
test.it("aaaabcc encoded should have length 10")
def test_len(res):
    test.assert_not_equals(res, None)
    test.assert_equals(len(res), 10)
test_len(encode(fs, "aaaabcc"))

test.it("empty list encode")
test.assert_equals(encode(fs, []), '')

test.it("empty list decode")
test.assert_equals(decode(fs, []), '')

def test_enc_len(fs, strs, lens):
    def enc_len(s):
        return len(encode(fs, s))
    test.assert_equals(list(map(enc_len, strs)), lens)

test.describe("length")
test.it("equal lengths with same frequencies if alphabet size is a power of two")
test_enc_len([('a', 1), ('b', 1)], ["a", "b"], [1, 1])

test.it("smaller length for higher frequency, if size of alphabet is not power of two")
test_enc_len([('a', 1), ('b', 1), ('c', 2)], ["a", "b", "c"], [2, 2, 1])

test.describe("error handling")
s = "aaaabcc"
fs = frequencies(s)
test.assert_equals( sorted(fs), [ ("a",4), ("b",1), ("c",2) ] )
test_enc_len(fs, [s], [10])
test.assert_equals( encode( fs, "" ), "" )
test.assert_equals( decode( fs, "" ), "" )

test.assert_equals( encode( [], "" ), None );
test.assert_equals( decode( [], "" ), None );
test.assert_equals( encode( [('a', 1)], "" ), None );
test.assert_equals( decode( [('a', 1)], "" ), None );
"""