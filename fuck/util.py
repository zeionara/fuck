import re

from pymorphy3 import MorphAnalyzer

PROFANE_WORDS_PATH = 'assets/profane-words.txt'

morph = MorphAnalyzer(lang = 'ru')


replacements = {
    'а': ('а', 'a'),
    'б': ('б', '6'),
    'в': ('в', ),
    'г': ('г', ),
    'д': ('д', ),
    'е': ('е', 'e'),
    'ё': ('ё', 'е', 'e'),
    'ж': ('ж', ),
    'з': ('з', '3'),
    'и': ('и', ),
    'й': ('й', ),
    'к': ('к', ),
    'л': ('л', ),
    'м': ('м', ),
    'н': ('н', 'h'),
    'о': ('о', 'o'),
    'п': ('п'),
    'р': ('р', 'p'),
    'с': ('с', 'c'),
    'т': ('т', 't'),
    'у': ('у', 'y'),
    'ф': ('ф', ),
    'х': ('х', 'x'),
    'ц': ('ц', ),
    'ч': ('ч', ),
    'ш': ('ш', ),
    'щ': ('щ', ),
    'ъ': ('ъ', 'ь'),
    'ы': ('ы'),
    'ь': ('ь', 'ъ'),
    'э': ('э'),
    'ю': ('ю'),
    'я': ('я')
}


def replace(token, prefix = '', index = 0):
    if index < len(token):
        for replacement in replacements.get(token[index], (token[index], )):
            for token_form in replace(token, prefix = f'{prefix}{replacement}', index = index + 1):
                yield token_form
    else:
        yield prefix


# EXCEPTIONS = ['хули', 'отъебись', 'заебись']
EXCEPTION_MARK = '*'


with open(PROFANE_WORDS_PATH, 'r', encoding = 'utf-8') as file:
    words = []

    for word in file.read().split('\n'):
        if word:
            parts = word.split(EXCEPTION_MARK, maxsplit = 1)
            word = parts[0]

            if len(parts) > 1:
                for variant in replace(word):
                    words.append(variant)
            else:
                forms = morph.parse(word)

                if len(forms) > 0:
                    for lexeme in forms[0].lexeme:
                        for variant in replace(lexeme.word):
                            words.append(variant)

    PROFANE_WORDS = words

    # PROFANE_WORDS = words if words[-1] else words[:-1]


def restore_shape(template: str, replacement: str):
    if re.fullmatch(template, replacement):
        return replacement

    if re.fullmatch(template, capitalized := replacement.capitalize()):
        return capitalized

    if re.fullmatch(template, upper := replacement.upper()):
        return upper

    return replacement
