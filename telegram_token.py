import keyring


def telegram_token(is_production=False):
    """
    Retrieves the Telegram token from the macOS keychain.
    Ensure the token is stored in the keychain with the service name 'telegram' and key 'bot_token'.
    """
    if not is_production:
        return keyring.get_password("IlmariLatijnDevBot", "IlmariLatijnDevBot")
    return keyring.get_password("IlmariLatijnBot", "IlmariLatijnBot")


def set_telegram_token(token):
    """
    Sets the Telegram token in the macOS keychain.
    Use this function to store the token securely.
    """
    keyring.set_password("IlmariLatijnBot", "IlmariLatijnBot", token)
    print("Telegram token set successfully.")
