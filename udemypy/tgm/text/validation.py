# Telegram Special Characters
SPECIAL_CHARS = ('_', '*',
                 '[', ']',
                 '(', ')',
                 '~', '`',
                 '>', '#',
                 '+', '-',
                 '=', '|',
                 '{', '}',
                 '.', '!')


def get_valid_msg(msg):
    '''
    Returns the msg but with a backslash added behind all special characters  
    '''
    valid_msg = ''
    for character in str(msg):
        if character in SPECIAL_CHARS:
            valid_msg += f'\\{character}'
        else:
            valid_msg += character

    return valid_msg
