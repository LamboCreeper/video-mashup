chars = [
    "a", "b", "c", "d", "e", "f",
    "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r",
    "s", "t", "u", "v", "w", "x",
    "y", "z"
]


def strip_punctuation(string: str):
    no_punctuation = ""

    for letter in string:
        for char in chars:
            if char == letter:
                no_punctuation += letter

    return no_punctuation
