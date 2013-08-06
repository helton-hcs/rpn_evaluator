# -*- coding: utf-8 -*-

import re
import collections

tokens_patterns = [
 ('NUMBER',    r'\d+(\.\d+([Ee]\d+)?)?'),
 ('OP_PLUS',   r'\+'),
 ('OP_MINUS',  r'\-'),
 ('OP_EXP',    r'\*\*'), 
 ('OP_MOD',    r'\%'),
 ('OP_TIMES',  r'\*'),
 ('OP_DIVIDE', r'/'),
 ('SQRT',      r'sqrt'),
 ('SKIP',      r'[ \t\n]+'),
]

Token = collections.namedtuple('Token', 'type value')

def tokenizer(expression):
    get_token = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens_patterns)).search
    position = 0
    token = get_token(expression)
    while token:        
      token_type = token.lastgroup
      if token_type != 'SKIP':
          token_value = token.group(token_type)
          yield Token(token_type, token_value)
      token = get_token(expression, token.end())

def print_tokens(expression):
    print('Tokens: ')
    for token in tokenizer(expression):
        print(token)

def evaluate(expression):
    stack = []
    for token in tokenizer(expression):
        if token.type == 'NUMBER':
            stack.append(float(token.value))
        else:
            if token.type == 'SQRT':
                stack.append(float(stack.pop() ** (1 / 2)))
            else:
                value2 = stack.pop()
                value1 = stack.pop()
                if token.type == 'OP_PLUS':
                    stack.append(float(value1 + value2))
                elif token.type == 'OP_MINUS':
                    stack.append(float(value1 - value2))
                elif token.type == 'OP_TIMES':
                    stack.append(float(value1 * value2))
                elif token.type == 'OP_EXP':
                    stack.append(float(value1 ** value2))
                elif token.type == 'OP_MOD':
                    stack.append(float(value1 % value2))
                elif token.type == 'OP_DIVIDE':                
                    if value2 == 0:
                        raise ValueError('Division by zero')
                    else:
                        stack.append(float(value1 / value2))
    return stack.pop()

def solve(expression):
    print('Expression: ', expression)
    print('Result: ', evaluate(expression))
    print('=' * 50)

if __name__ == '__main__':
    solve('1123 2 - 4 +')
    solve('5 1 2 + 4 * + 3 -')
    solve('3.14 0.14 - 3 *')
    solve('2 11 **')
    solve('2 11 %')
    solve('49 sqrt')
    solve('3 2 ** 4 2 ** + sqrt')

# print_tokens('5 1 2 + 4 * + 3 -')
