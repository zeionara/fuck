import re

PROFANE_WORDS_PATH = 'assets/profane-words.txt'

with open(PROFANE_WORDS_PATH, 'r', encoding = 'utf-8') as file:
    PROFANE_WORDS = file.read().split('\n')


def restore_shape(template: str, replacement: str):
    if re.fullmatch(template, replacement):
        return replacement

    if re.fullmatch(template, capitalized := replacement.capitalize()):
        return capitalized

    if re.fullmatch(template, upper := replacement.upper()):
        return upper

    return replacement
