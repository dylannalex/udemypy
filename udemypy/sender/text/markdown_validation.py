# Markdown special characters
SPECIAL_CHARS = (
    "_",
    "*",
    "[",
    "]",
    "(",
    ")",
    "~",
    "`",
    ">",
    "#",
    "+",
    "-",
    "=",
    "|",
    "{",
    "}",
    ".",
    "!",
)


def get_valid_text(text):
    """
    Returns the text but with a backslash added behind all special characters
    """
    valid_text = ""
    for character in str(text):
        if character in SPECIAL_CHARS:
            valid_text += f"\\{character}"
        else:
            valid_text += character

    return valid_text
