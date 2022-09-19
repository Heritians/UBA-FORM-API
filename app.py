from fastapi import FastAPI
from API.utils.DBConnection import Singleton
app = FastAPI()

if __name__ == '__main__':
    try:
        s=Singleton()
        print(s.get_client())
    except Exception as e:
        print(e)


