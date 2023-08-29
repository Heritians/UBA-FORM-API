'''
This module contains LRU Cache implementation using Ordered dictionaries.

Used hashmap for faster access and queue for mantaining the access order so that the Least Recently Used data can be evicted.

The cache code uses:
    - a mutex lock to ensure that the cache is thread-safe. This is important, as the cache can be accessed by multiple threads at the same time.
    - an OrderedDict instead of a regular dictionary. This ensures that the entries in the cache are stored in the order in which they were added, 
    which is important for the LRU eviction policy.

'''

from collections import OrderedDict
import threading

class LoginCache:
    def __init__(self):
        """
        Creates a new user cache using an ordered dictionary
        """
        self.cache = OrderedDict()
        self.lock = threading.RLock()

    def get(self, aadhaar_number):
        """
        Gets the user information for the specified aadhaar number and updates the LRU cache element order accordingly.

        Args:
            aadhaar_number: The aadhaar number of the user.

        Returns:
            The user information, or None if the user is not found.
        """
        with self.lock:
            val = self.cache.get(aadhaar_number)
            if(val):
                self.cache.move_to_end(val)
            return val

    def set(self, aadhaar_number, login_credentials):
        """
        Sets the user information for the specified aadhaar number and if the cache if full then evicts an element as per the LRU eviction policy.

        Args:
            aadhaar_number: The aadhaar number of the user.
            login_credentials: The user's login credentials.
        """
        with self.lock:
            if(len(self.cache)<100):
                self.cache[aadhaar_number] = login_credentials
            else:
                self.evict()
                self.cache[aadhaar_number] = login_credentials

    def evict(self):
        """
        Removes the least recently used user from the cache.

        Returns:
            The least recently used user, or None if the cache is empty.
        """
        with self.lock:
            return self.cache.popitem(last=False)

LRUcache = LoginCache()