from sys import argv
from udemypy.text import emojis
from udemypy.text.markdown_validation import get_valid_text
from udemypy.tgm import tgm_bot


SUPPORT_MSG = f"""{emojis.HEART} Hope you are all enjoying all these free courses!

If you like this community and you want to help me improving this channel you can:

{emojis.SPARKLES} Share this channel with your friends
{emojis.SPARKLES} Send me new features ideas to udemypy21@gmail.com
{emojis.SPARKLES} Donate me via:
{emojis.STAR} PayPal: https://bit.ly/paypalUdemyPy
{emojis.STAR} Mercado Libre: 
    CVU: 0000003100050801781859
    Alias: dylan.tinten"""
MESSAGES = {"support": SUPPORT_MSG}


def send_message(msg):
    tgm_bot.send_message(get_valid_text(MESSAGES[msg]))


if __name__ == "__main__":
    send_message(argv[1])
