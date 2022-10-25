# troubleshooting 
from DBConnection import DBConnection
DBConnection()
client=DBConnection.get_client()
# client.drop_database("Sehore")
print(client.list_database_names())