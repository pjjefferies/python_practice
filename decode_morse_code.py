# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 22:18:08 2019

@author: PaulJ
"""

import unittest


def decodeMorse(morse_code):
    code_words = morse_code.upper().strip().split('   ')
    letters = []
    for code_word in code_words:
        letters += [MORSE_CODE[letter] for letter in code_word.split()] + [' ']
    return ''.join(letters[:-1])


MORSE_CODE = {'.-': 'A',
              '-...': 'B',
              '-.-.': 'C',
              '-..': 'D',
              '.': 'E',
              '..-.': 'F',
              '--.': 'G',
              '....': 'H',
              '..': 'I',
              '.---': 'J',
              '-.-': 'K',
              '.-..': 'L',
              '--': 'M',
              '-.': 'N',
              '---': 'O',
              '.--.': 'P',
              '--.-': 'Q',
              '.-.': 'R',
              '...': 'S',
              '-': 'T',
              '..-': 'U',
              '...-': 'V',
              '.--': 'W',
              '-..-': 'X',
              '-.--': 'Y',
              '--..': 'Z',
              '-----': '0',
              '.----': '1',
              '..---': '2',
              '...--': '3',
              '....-': '4',
              '.....': '5',
              '-....': '6',
              '--...': '7',
              '---..': '8',
              '----.': '9',
              '.-.-.-': '.',
              '--..--': ',',
              '..--..': '?',
              '.----.': "'",
              '-.-.--': '!',
              '-..-.': '/',
              '-.--.': '(',
              '-.--.-': ')',
              '.-...': '&',
              '---...': ':',
              '-.-.-.': ';',
              '-...-': '=',
              '.-.-.': '+',
              '-....-': '-',
              '..--.-': '_',
              '.-..-.': '"',
              '...-..-': '$',
              '.--.-.': '@',
              '...-.-': 'End of Work',
              '........': 'Error',
              # '-.-': 'Invitation to Transmit',
              '-.-.-': 'Starting Signal',
              # '.-.-.': 'New Page Signal',
              '...-.': 'Understood',
              # '.-...': 'Wait',
              '...---...': 'SOS'
              }


class InterpreterTestMethods(unittest.TestCase):

    tests = {'.... . -.--   .--- ..- -.. .': 'HEY JUDE',
             ' . ': 'E',
             '   .   . ': 'E E',
             '      ...---... -.-.--   - .... .   --.- ..- .. -.-. -.-   -... .-. --- .-- -.   ..-. --- -..-   .--- ..- -- .--. ...   --- ...- . .-.   - .... .   .-.. .- --.. -.--   -.. --- --. .-.-.-  ': 'SOS! THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.'
             }

    def test_basic(self):
        for code in self.tests:
            answer = self.tests[code]
            result = decodeMorse(code)
            print('code:', code, ', answer:', answer,
                  ', result:', result)
            self.assertEqual(result, answer)


if __name__ == '__main__':
    unittest.main()
