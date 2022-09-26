from .DBConnection import DBConnection


class DBQueries:

    @classmethod
    def insert_to_database(cls, db_name, coll_name, data):
        """insert records"""
        con = DBConnection.get_client()
        mydb = con[db_name]
        mycol = mydb[coll_name]

        if isinstance(data, list):
            return mycol.insert_many(data)
        else:
            return mycol.insert_one(data)

    @classmethod
    def count_all_documents(cls, db_name, coll_name):
        """count dcouments in collection"""
        con = DBConnection.get_client()

        mydb = con[db_name]
        mycol = mydb[coll_name]
        return mycol.count_documents({})

    @classmethod
    def fetch_last(cls, db_name, coll_name):
        con = DBConnection.get_client()

        mydb = con[db_name]
        mycol = mydb[coll_name]

        return mycol.find().sort('_id', -1)[0]

    @classmethod
    def retrieve_documents(cls, db_name):
        con = DBConnection.get_client()
        mydb = con[db_name]
        response_data = {}
        response_data["data"] = {}

        for cols in mydb.list_collection_names():
            mycol = mydb[cols]
            # print(type(mycol))
            # print(mycol)
            li = [docs for docs in mycol.find({})]
            response_data["data"].update({mycol.full_name.split('.')[-1]: li})
            # pprint.pprint(mycol.full_name)
            # print(type(mycol.full_name))
        return response_data
