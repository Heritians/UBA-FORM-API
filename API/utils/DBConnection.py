""" Import Important Packages"""
from pymongo import MongoClient

from API.core.ConfigEnv import settings

database_uri = settings.DATABASE_URI

class DBConnection:
    """DBConnection Class. It ensures only one instance of the class is 
       created and it is accessible from everywhere. It is used in the 
       design of logging classes, Configuration classes where we need to have 
       only one instance of the class. There is no need to create multiple 
       instances of each operation across all components of application.

    Raises:
           Exception: It raises an exception if the client instance is not created.
    """
    __client = None #This is the client variable that is used to connect to the database
    flag = False
    def __init__(self):
        """This is the constructor of the class. It is used to create the client 
        variable. It also checks if the client instance is already created. 
        If the client instance is already created, then it does not create a 
        new client instance.
        """
        if DBConnection.__client is not None:
            raise Exception("This class is a singleton!")
        else:    
            DBConnection.__client = MongoClient(database_uri)
            DBConnection.flag = True

    @staticmethod  # A static method is a method that is called without creating an instance of the class.
    def get_client():
        """The get_client() function is used to get the client instance.

        Returns:
            DBConnection.__client: It returns the client instance.
        """
        return DBConnection.__client






