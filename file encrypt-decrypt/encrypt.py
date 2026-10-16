import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Configuration Constants
CHUNK_SIZE = 64 * 1024  # 64KB chunks for memory efficiency
SALT_SIZE = 16          # 128-bit salt
NONCE_SIZE = 12         # Standard nonce size for AES-GCM

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a secure 256-bit AES key from a password using Scrypt."""
    kdf = Scrypt(
        salt=salt,
        length=32,       # 32 bytes = 256-bit key
        n=2**14,         # CPU/memory cost factor
        r=8,             # Block size
        p=1              # Parallelization factor
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, password: str):
    """Encrypts a file securely using AES-256-GCM."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    output_path = file_path + ".enc"
    
    with open(file_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        # 1. Write the metadata (Salt and Nonce) to the very front of the file
        f_out.write(salt)
        f_out.write(nonce)
        
        # 2. Encrypt and write the data in chunks
        while chunk := f_in.read(CHUNK_SIZE):
            # We pass the salt as associated data to bind it to the payload
            encrypted_chunk = aesgcm.encrypt(nonce, chunk, associated_data=salt)
            f_out.write(encrypted_chunk)
            
    print(file_path, "successfully encrypted to", output_path)

def decrypt_file(file_path: str, password: str):
    """Decrypts a file securely and verifies its integrity."""
    output_path = file_path.replace(".enc", ".dec") if file_path.endswith(".enc") else file_path + ".dec"

    with open(file_path, 'rb') as f_in:
        # 1. Read the metadata back out
        salt = f_in.read(SALT_SIZE)
        nonce = f_in.read(NONCE_SIZE)
        
        # 2. Re-derive the exact same key using the extracted salt
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        
        # Calculate encrypted chunk size (AES-GCM adds a 16-byte authentication tag)
        encrypted_chunk_size = CHUNK_SIZE + 16 
        
        with open(output_path, 'wb') as f_out:
            try:
                while chunk := f_in.read(encrypted_chunk_size):
                    decrypted_chunk = aesgcm.decrypt(nonce, chunk, associated_data=salt)
                    f_out.write(decrypted_chunk)
                print(file_path, "successfully decrypted to", output_path)
            except Exception as e:
                print("Decryption Failed! The file has been altered or the password is wrong.")

# --- Quick Test ---
if __name__ == "__main__":
    secret_password = "SuperSecurePassword123!"
    sample_file = "resume_manishroy.docx"
    
    # Create a dummy file
    with open(sample_file, "w") as f:
        f.write("This is highly sensitive data that must be protected at all costs.")
        
    # Execute routine
    encrypt_file(sample_file, secret_password)
    decrypt_file(sample_file + ".enc", secret_password)
