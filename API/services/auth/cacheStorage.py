from collections import OrderedDict
import hashlib

class UserCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def register_user(self, username, role, aadhar, password, village_name):
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        hashed_password = self._hash_password(password)  # Hash the password before storing it
        self.cache[username] = {
            'role': role,
            'aadhar': aadhar,
            'hashed_password': hashed_password,
            'village_name': village_name
        }

    def authenticate_user(self, username, password):
        if username in self.cache:
            user_info = self.cache[username]
            if self._verify_password(password, user_info['hashed_password']):
                return user_info['role'], user_info['aadhar'], user_info['village_name']
        return None, None, None

    def _hash_password(self, password):
        # You can use a stronger password hashing library in practice, such as bcrypt
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, input_password, stored_hashed_password):
        input_hashed_password = self._hash_password(input_password)
        return input_hashed_password == stored_hashed_password