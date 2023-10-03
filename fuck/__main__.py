import re

from click import group, argument
from pandas import read_csv

from .util import PROFANE_WORDS, restore_shape


CENSORING_SEQUENCE = r'[*@%]+'
CENSORING_SEQUENCE_TEMPLATE = re.compile(CENSORING_SEQUENCE)
CENSORED_TOKEN_STRICT_TEMPLATE = re.compile(f'[а-яА-ЯёЁa-zA-Z6]+(?:{CENSORING_SEQUENCE}[а-яА-ЯёЁa-zA-Z6]+)+')

MIN = 30
MAX = 35

# CENSORED_TOKEN_LEFT_ONLY_TEMPLATE = re.compile(r'[а-яА-ЯёЁ]+[*@]+(?:\S+)?')
# CENSORED_TOKEN_RIGHT_ONLY_TEMPLATE = re.compile(r'(?:\S+)?[*@]+[а-яА-ЯёЁ]+')


@group()
def main():
    pass


@main.command()
@argument('path', type = str, default = 'assets/anecdotes.tsv')
def stats(path: str):
    df = read_csv(path, sep = '\t')

    n_censored_texts = 0

    for text in df['text']:

        if len(matches := CENSORED_TOKEN_STRICT_TEMPLATE.findall(text)) > 0:
            original_text = text

            verbose = MIN <= n_censored_texts < MAX

            if verbose:
                print(original_text)

            # print(text)
            for match in matches:

                if verbose:
                    print('> ', match)

                template = CENSORING_SEQUENCE_TEMPLATE.sub('.*', match)
                lower_template = CENSORING_SEQUENCE_TEMPLATE.sub('.*', match.lower())

                # print(template)

                replacement = None

                for token in PROFANE_WORDS:
                    if re.fullmatch(lower_template, token) is not None:
                        replacement = restore_shape(template, token)
                        break

                # if verbose:
                #     print(restore_shape(template, replacement))

                if replacement is not None:
                    if verbose:
                        print('< ', replacement)
                    text = text.replace(match, replacement)

            n_censored_texts += 1

            if verbose:
                print(text)
                print('-' * 100)

        # elif (match := CENSORED_TOKEN_LEFT_ONLY_TEMPLATE.search(text)) is not None:
        #     print(text)
        #     print(match)
        # elif (match := CENSORED_TOKEN_RIGHT_ONLY_TEMPLATE.search(text)) is not None:
        #     print(text)
        #     print(match)

    print(f'Found {n_censored_texts} censored texts')


if __name__ == '__main__':
    main()
