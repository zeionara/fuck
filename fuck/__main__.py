import re

from click import group, argument
from pandas import read_csv

from .util import CENSORED_TOKENS


CENSORING_SEQUENCE = r'[*@%]+'
CENSORING_SEQUENCE_TEMPLATE = re.compile(CENSORING_SEQUENCE)
CENSORED_TOKEN_STRICT_TEMPLATE = re.compile(f'[а-яА-ЯёЁ]+{CENSORING_SEQUENCE}[а-яА-ЯёЁ]+')

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
        original_text = text

        if len(matches := CENSORED_TOKEN_STRICT_TEMPLATE.findall(text)) > 0:
            # print(text)
            for match in matches:
                template = CENSORING_SEQUENCE_TEMPLATE.sub('.*', match)

                # print(template)

                replacement = None

                for token in CENSORED_TOKENS:
                    if re.fullmatch(template, token) is not None:
                        replacement = token
                        break

                if replacement is not None:
                    text = text.replace(match, replacement)

            n_censored_texts += 1

            print(original_text)
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
