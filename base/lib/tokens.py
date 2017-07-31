from secrets import token_urlsafe

def generate_token(length=8):
    return token_urlsafe(length)