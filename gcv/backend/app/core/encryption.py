from cryptography.fernet import Fernet
from .config import settings

# Idealmente, a chave de criptografia seria gerenciada de forma mais segura (ex: Vault)
# Por simplicidade, vamos derivá-la da SECRET_KEY da aplicação.
# ATENÇÃO: Mudar a SECRET_KEY invalidará os dados criptografados.
key = settings.SECRET_KEY.encode()
# A chave precisa ter 32 bytes para Fernet
if len(key) < 32:
    key = key + b' ' * (32 - len(key))
key = key[:32]

cipher_suite = Fernet(key)

def encrypt_data(data: str) -> str:
    """Criptografa uma string."""
    if not data:
        return ""
    encrypted_bytes = cipher_suite.encrypt(data.encode())
    return encrypted_bytes.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Descriptografa uma string."""
    if not encrypted_data:
        return ""
    decrypted_bytes = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted_bytes.decode()
