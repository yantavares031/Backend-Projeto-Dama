from abc import ABC, abstractmethod
from bcrypt import hashpw, checkpw, gensalt

class Cryptography(ABC):

    @abstractmethod
    def hash_password(password):
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        return hashed_password
    
    @abstractmethod
    def check_password(password_attempt, stored_hashed_password):
        return checkpw(password_attempt.encode('utf-8'), stored_hashed_password)