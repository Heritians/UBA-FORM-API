from fastapi import FastAPI
from API.utils.DBConnection import DBConnection
# from dotenv import load_dotenv
# load_dotenv()


app = FastAPI()

from API import fwapp

# inits
try:
    dbconnection = DBConnection()
    print(f"Connection successful:{dbconnection.get_client()}")
except Exception as e:
    print(e)

