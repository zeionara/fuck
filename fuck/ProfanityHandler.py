import re
import os

from pymorphy3 import MorphAnalyzer
from tqdm import tqdm

from .util import make_forms, restore_shape, CENSORED_TOKEN_TEMPLATE, to_template

EXCEPTION_MARK = '*'
SPACE = ' '

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profane-words.txt')


class ProfanityHandler:
    def __init__(self, path: str = None, verbose: bool = False):
        if path is None:
            path = DEFAULT_PATH

        self.path = path
        self.morph = morph = MorphAnalyzer(lang = 'ru')

        with open(path, 'r', encoding = 'utf-8') as file:
            words = []
            replacements = {}

            lines = file.read().split('\n')
            pbar = tqdm(total = len(lines), desc = 'Loading profane words dictionary') if verbose else None

            for word in lines:
                if word and not word.startswith('#'):  # skip comments
                    replacement = None

                    parts = word.split(SPACE, maxsplit = 1)  # handle custom replacements

                    if len(parts) > 1:
                        word = parts[0]
                        replacement = parts[1]

                    parts = word.split(EXCEPTION_MARK, maxsplit = 1)  # handle exceptions (exceptions must not be expanded by the morph analyzer)
                    word = parts[0]

                    if len(parts) > 1:
                        for form in make_forms(word):
                            words.append(form)

                            replacements[form] = word if replacement is None else replacement
                    else:
                        entries = morph.parse(word)

                        if len(entries) > 0:
                            for lexeme in entries[0].lexeme:
                                for form in make_forms(word := lexeme.word):
                                    words.append(form)

                                    replacements[form] = word if replacement is None else replacement

                if verbose:
                    pbar.update()

        self.words = words
        self.replacements = replacements

        if verbose:
            pbar.desc = f'Loaded {len(words)} word forms'

    def _match(self, template: str, normalized_template: str):
        for word in self.words:
            if re.fullmatch(normalized_template, word) is not None:
                return restore_shape(template, word)

        return None

    def _replace(self, text: str, word: str):
        template = to_template(word)
        normalized_template = to_template(word.lower())

        match = self._match(template, normalized_template)

        if match is None:
            return text, False

        return text.replace(word, self.replacements.get(match, match)), True

    def uncensor(self, text: str):
        censored = False
        unhandled_matches = []

        for match in CENSORED_TOKEN_TEMPLATE.findall(text):
            text, found_replacement = self._replace(text, match)

            if not found_replacement:
                unhandled_matches.append(match)

            if censored is False:
                censored = True

        return text, censored, unhandled_matches

    @property
    def length(self):
        return len(self.words)
