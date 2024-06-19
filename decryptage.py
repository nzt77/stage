from cryptography.fernet import Fernet


SECRET_KEY = b'jIWK3ZjOfN_Lsn_Z1pZzzCgOG7Fd7Jpxn-K25K42FCs='
cipher = Fernet(SECRET_KEY)

def decrypt_data(encrypted_data: str) -> str:
    decrypted_data = cipher.decrypt(encrypted_data.encode()).decode()
    transaction_data = decrypted_data.split('|')
    return '|'.join(transaction_data[:4]) 

if __name__ == "__main__":
    encrypted_data = input("Entrez le cryptage : ")
    try:
        decrypted_data = decrypt_data(encrypted_data)
        print(f"Data decryptées : {decrypted_data}")
    except Exception as e:
        print(f"Erreur: {e}")
