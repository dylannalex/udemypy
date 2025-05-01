from udemypy.sender.bot import SenderBot
try:
    from udemypy.sender.whatsapp_bot import WhatsAppBot
except ImportError:
    WhatsAppBot = None
    print(
        "[Warning] WhatsApp Bot not available."
    )
try:
    from udemypy.sender.tgm_bot import TelegramBot
except ImportError:
    TelegramBot = None
    print(
        "[Warning] Telegram Bot not available."
    )
try:
    from udemypy.sender.twitter_bot import TwitterBot
except ImportError:
    TwitterBot = None
    print(
        "[Warning] Twitter Bot not available."
    )