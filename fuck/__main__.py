import re

from click import group, argument, option
from pandas import read_csv
from tqdm import tqdm

from .util import restore_shape
from .ProfanityHandler import ProfanityHandler


MIN = 0
N = 5

# CENSORED_TOKEN_LEFT_ONLY_TEMPLATE = re.compile(r'[а-яА-ЯёЁ]+[*@]+(?:\S+)?')
# CENSORED_TOKEN_RIGHT_ONLY_TEMPLATE = re.compile(r'(?:\S+)?[*@]+[а-яА-ЯёЁ]+')


@group()
def main():
    pass


@main.command()
@argument('path', type = str, default = 'assets/anecdotes.tsv')
@option('--dictionary', '-d', type = str, default = 'assets/profane-words.txt')
@option('--verbose', '-v', is_flag = True)
def stats(path: str, dictionary: str, verbose: bool):
    # print(len(PROFANE_WORDS))

    ph = ProfanityHandler(path = dictionary, verbose = verbose)
    df = read_csv(path, sep = '\t')

    n_censored_texts = 0
    # n_unhandled_matches = 0

    unhandled_matches = []

    pbar = tqdm(total = len(df.index), desc = 'Handling documents') if verbose else None

    # updated_texts = []

    for text in df['text']:
        _, censored, matches = ph.uncensor(text)

        # if changed:
        #     print(text)
        #     print(uncensored_text)

        unhandled_matches.extend(matches)

        if censored:
            n_censored_texts += 1

        # if len(matches := CENSORED_TOKEN_STRICT_TEMPLATE.findall(text)) > 0:
        #     original_text = text

        #     # verbose = MIN <= n_censored_texts < (MIN + N)

        #     # if verbose:
        #     #     print(original_text)

        #     # print(text)
        #     for match in matches:

        #         # if verbose:
        #         #     print('> ', match)

        #         template = CENSORING_SEQUENCE_TEMPLATE.sub('.*', match)
        #         lower_template = CENSORING_SEQUENCE_TEMPLATE.sub('.*', match.lower())

        #         # print(template)

        #         replacement = None

        #         for token in PROFANE_WORDS:
        #             if re.fullmatch(lower_template, token) is not None:
        #                 replacement = restore_shape(template, token)
        #                 break

        #         # if verbose:
        #         #     print(restore_shape(template, replacement))

        #         if replacement is not None:
        #             # if verbose:
        #             #     print('< ', replacement)
        #             text = text.replace(match, replacement)
        #             print(original_text)
        #             print(text)
        #         else:
        #             # print('> ', match)
        #             # print('= ', original_text)
        #             # print('-' * 10)
        #             n_unhandled_matches += 1

        #     n_censored_texts += 1

        #     # if verbose:
        #     #     print(text)
        #     #     print('-' * 100)

        # updated_texts.append(text)

        # elif (match := CENSORED_TOKEN_LEFT_ONLY_TEMPLATE.search(text)) is not None:
        #     print(text)
        #     print(match)
        # elif (match := CENSORED_TOKEN_RIGHT_ONLY_TEMPLATE.search(text)) is not None:
        #     print(text)
        #     print(match)

        if verbose:
            pbar.update()

    # df['text'] = updated_texts
    # df.to_csv('assets/anecdotes-uncensored.csv', sep = '\t', index = False)

    print(f'Found {n_censored_texts} censored texts')
    print(f'Found {len(unhandled_matches)} unhandled matches: {", ".join(unhandled_matches)}')


if __name__ == '__main__':
    main()
