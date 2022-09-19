from fastapi import FastAPI
from API.utils.DBConnection import DBConnection
app = FastAPI()

if __name__ == '__main__':
    try:
        dbconnection=DBConnection()
        print(f"Connection successful:{dbconnection.get_client()}")
    except Exception as e:
        print(e)


