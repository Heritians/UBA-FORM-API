from .DBConnection import DBConnection


class DBQueries():


    @classmethod
    def insert_to_database(cls, db_name, coll_name, data):
        """insert records"""
        con = DBConnection.get_client()
        print(con)
        mydb = con[db_name]
        mycol = mydb[coll_name]

        if type(data) is list:
            return mycol.insert_many(data)
        else:
            return mycol.insert_one(data)
        # to-do

    @classmethod
    def count_all_documents(cls, db_name, coll_name):
        """count dcouments in collection"""
        mydb = DBQueries.con.client[db_name]
        mycol = mydb[coll_name]
        return mycol.count_documents({})
