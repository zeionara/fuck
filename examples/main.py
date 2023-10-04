from fuck import ProfanityHandler

text, censored, unhandled_matches = ProfanityHandler(
    path = 'assets/profane-words.txt'
).uncensor(
    'Нах**я до%@я нах%ярил??? Расх*%яривай нах@й - не д0х*ярим. Них*я, не дох@я дох%ярим - пох*ярили'
)

print(text)
print(censored)
print(unhandled_matches)
