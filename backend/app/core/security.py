from pwdlib import PasswordHash

'''
PasswordHash.recommended() automatically configures a secure password hasher 
(typically Argon2id), so you don't need to manually set up Argon2.
'''
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)