"""The __init__.py files are required to make Python treat directories 
containing the file as packages. This prevents directories with a common name, 
such as string, unintentionally hiding valid modules that occur later on the 
module search path. In the simplest case, __init__.py can just be an empty file, 
but it can also execute initialization code for the package.

The __init__.py file is the first file to be executed when a module is
imported. It is executed only once, when the module is first imported. It
defines the module's namespace and can be used to perform initialization
actions that are required to be performed only once.
"""

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

