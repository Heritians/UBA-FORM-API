import pymongo.cursor

from .DBConnection import DBConnection
from ..core.Exceptions import *

# fix ObjectId & FastApi conflict
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


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
        return response_data
        
    #Allow frontend to query data of a particular family via respondents_id      
    @classmethod
    def retrieve__id(cls, db_name, respondent_id, response_result):
        con = DBConnection.get_client()
        mydb = con[db_name]
        metacol = mydb['meta']
        respcol=mydb['respondent_prof']
        li = [docs for docs in metacol.find({"resp_id": respondent_id})]
        if len(li) == 0:
            raise InfoNotFoundException(response_result,
                                        "family with this respondent id does not exist in the database")

        #get respondent_id from the meta collection
        resp_id=li[0]['resp_id']
        respli=[docs for docs in respcol.find({"id_no": resp_id})]
        #get __id from the respondent_prof collection
        return respli[0]['__id']
        
    @classmethod
    def retrieve_documents_by_id(cls, db_name,respondent_id, response_result):
        con = DBConnection.get_client()
        mydb = con[db_name]
        response_data = {}
        response_data["data"] = {}
        __id=cls.retrieve__id(db_name,respondent_id, response_result)
        for cols in mydb.list_collection_names():
            if cols=="meta":
                continue
            mycol = mydb[cols]
            li = [docs for docs in cls.filtered_db_search(db_name,cols,['__id','_id'],__id=__id)]
            response_data["data"].update({mycol.full_name.split('.')[-1]: li})
        return response_data


    @classmethod
    def filtered_db_search(cls, db_name, coll_name,fields_to_drop ,**kwargs) -> pymongo.cursor.Cursor:
        con = DBConnection.get_client()

        mydb = con[db_name]
        mycol = mydb[coll_name]
        cursor = mycol.find(kwargs,{i:0 for i in fields_to_drop})

        return cursor

    @classmethod
    def fetch_indiv_document(cls,db_name,respondent_id, response_result):
        indivdata = [docs for docs in cls.filtered_db_search(db_name,'fam_info',['__id','_id'],AADHAR_No=respondent_id)]
        if len(indivdata) == 0:
            raise InfoNotFoundException(response_result, "person with this id does not exist in the database")
        return indivdata[0]

        