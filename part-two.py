#!/usr/bin/env python3

import os
from time import perf_counter_ns

class PatternMatcher:
    def __init__(self, parameters):
        pattern = map(int,parameters.split(','))
        self.states = ['.']
        for element in pattern:
            for _ in range(element):
                self.states.append('#')
            self.states.append('.')
        self.valid_states = {0: 1}

    def state_accept(self, index, char):
        current_state = self.states[index]
        next_state = self.states[index + 1] if index < len(self.states) - 1 else None
        if char == '#':
            if next_state == '#':
                return [index + 1]
            else:
                return []
        elif char == '.':
            if current_state == '.':
                return [index]
            elif next_state == '.':
                return [index + 1]
            else:
                return []
        elif char == '?':
            if current_state == '.':
                if next_state:
                    return [index, index + 1]
                else:
                    return [index]
            elif next_state:
                return [index + 1]
            else:
                return []

    def process_char(self, char):
        new_states = {ix:0 for ix in range(len(self.states))}
        for state_id, count in self.valid_states.items():
            for new_state in self.state_accept(state_id, char):
                new_states[new_state] += count
        self.valid_states = {k:v for k,v in new_states.items() if v > 0}

    def solutions(self):
        return self.valid_states.get(len(self.states) - 1, 0) + self.valid_states.get(len(self.states) - 2, 0)

def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input_stream:
        data = input_stream.read().split('\n')

    answer = 0
    for line in data:
        pattern, definition = line.split(' ')
        pattern = '?'.join([pattern] * 5)
        definition = ','.join([definition] * 5)
        pattern = pattern.strip('.') + '.'
        pattern = '.'.join([p for p in pattern.split('.') if p != ''])
        matcher = PatternMatcher(definition)
        for c in pattern:
            matcher.process_char(c)
        answer += matcher.solutions()

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
