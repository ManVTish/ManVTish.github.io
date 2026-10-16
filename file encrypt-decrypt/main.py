import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(password: str, salt: bytes) -> bytes:
    """Turns your plain text password into a secure 256-bit key."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, password: str):
    """Encrypts a file and safely deletes the original version."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # 1. Read the original file data
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # 2. Generate random security numbers (Salt and Nonce)
    salt = os.urandom(16)
    nonce = os.urandom(12)

    # 3. Encrypt the data
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # 4. Save the encrypted data to a new file (.enc)
    output_path = file_path + ".enc"
    with open(output_path, "wb") as f:
        f.write(salt)
        f.write(nonce)
        f.write(ciphertext)

    # 5. Securely wipe the original file from your machine
    # Overwrite with random data first so it can't be recovered easily
    with open(file_path, "wb") as f:
        f.write(os.urandom(os.path.getsize(file_path)))
    os.remove(file_path)

    print(f"\n[SUCCESS] File encrypted!")
    print(f"Original file deleted. Protected file saved as: {output_path}")

def decrypt_file(file_path: str, password: str):
    """Decrypts a .enc file back to its original format."""
    if not file_path.endswith(".enc"):
        print("Error: You can only decrypt files that end with '.enc'")
        return
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # 1. Read the encrypted file pieces
    with open(file_path, "rb") as f:
        salt = f.read(16)
        nonce = f.read(12)
        ciphertext = f.read()

    # 2. Re-build the key using the password and the extracted salt
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        # 3. Try to decrypt
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        # 4. Save the restored file (removes the .enc extension)
        output_path = file_path[:-4]
        with open(output_path, "wb") as f:
            f.write(plaintext)
            
        # Remove the encrypted version now that it's open
        os.remove(file_path)
        print(f"\n[SUCCESS] File decrypted! Restored file: {output_path}")
        
    except Exception:
        print("\n[ERROR] Decryption failed! Wrong password, or the file was tampered with.")

# --- Simple User Interface ---
if __name__ == "__main__":
    print("=== Simple File Encryptor/Decryptor ===")
    action = input("Type 'E' to Encrypt or 'D' to Decrypt: ").strip().upper()
    
    if action not in ['E', 'D']:
        print("Invalid choice. Exiting.")
        sys.exit()
        
    target_file = input("Enter the full path to the file: ").strip().strip('"')
    user_password = input("Enter the secret password: ").strip()
    
    if action == 'E':
        encrypt_file(target_file, user_password)
    else:
        decrypt_file(target_file, user_password)

