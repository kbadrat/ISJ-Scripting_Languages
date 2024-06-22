#!/usr/bin/env python3

def gen_quiz(qpool, *indexes, altcodes = 'ABCDEF', quiz = None):

    altcodes = list(altcodes)
    result = [] if quiz is None else quiz

    for index in indexes:
        try:
            result.append((qpool[index][0], [': '.join(pair) for pair in zip(altcodes, qpool[index][1]) if pair[1] is not None]))
        except IndexError as exception:
            print(f"Ignoring index {index} - {exception}")
    return result
