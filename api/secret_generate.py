import secrets

def generate_secret_token(len_in_bytes: int) -> str:
    return secrets.token_hex(len_in_bytes)

length_in_bytes = 16
secret_token = generate_secret_token(length_in_bytes)
print(f"Секретний токен: {secret_token}")
