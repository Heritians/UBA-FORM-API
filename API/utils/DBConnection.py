""" Import Important Packages"""
import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient

database_uri=os.environ.get('DATABASE_URI') #Get the database URI

class Singleton:
    """ 
    Singleton Class. It ensures only one instance of the class is created and it is accessible from everywhere. It is used in the design of logging classes, Configuration classes where we need to have only one instance of the class. There is no need to create multiple instances of each operation across all components of application.
    """
    __client = None #This is the client variable that is used to connect to the database
    def __init__(self):
        """
        This is the constructor of the class. It is used to create the client variable. It also checks if the client instance is already created. If the client instance is already created, then it does not create a new client instance.
        """
        if Singleton.__client is not None:
            raise Exception("This class is a singleton!")
        else:    
            Singleton.__client = MongoClient(database_uri)  

    @staticmethod  # A static method is a method that is called without creating an instance of the class.
    def get_client():
        """
        The get_client() function is used to get the client instance. 
        """
        return Singleton.__client            
            

s=Singleton()
print(s.get_client())
print(s)            







