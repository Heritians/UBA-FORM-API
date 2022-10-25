from fastapi import FastAPI
from API.utils.DBConnection import DBConnection

app = FastAPI(title="Connecting Villages API",version="V0.1.0",description="API for Connecting Villages")

from API import fwapp

# inits
try:
    dbconnection = DBConnection()
    print(f"Connection successful:{dbconnection.get_client()}")
except Exception as e:
    print(e)

