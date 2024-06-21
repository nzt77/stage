from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_with_public_key(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

# Déchiffrement avec la clé privée
def decrypt_with_private_key(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message.encode()),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

# Affichage des clés en format PEM
def display_keys(private_key, public_key):
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    print(f"Private Key:\n{private_pem}")
    print(f"Public Key:\n{public_pem}")

def main():
    # Génération des clés
    private_key, public_key = generate_rsa_keys()
    
    # Affichage des clés
    display_keys(private_key, public_key)
    
    # Message à chiffrer
    message = "Hello, World!"
    print(f"Original Message: {message}")
    
    # Chiffrement
    encrypted_message = encrypt_with_public_key(public_key, message)
    print(f"Encrypted Message: {encrypted_message}")
    
    # Déchiffrement
    decrypted_message = decrypt_with_private_key(private_key, encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")

if __name__ == "__main__":
    main()
