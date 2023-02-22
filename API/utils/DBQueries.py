""" Queries script for the API. It is used to create the queries 
that are used to interact with the database. 
"""
import pymongo.cursor
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult,InsertManyResult
from pymongo.typings import _DocumentType

from typing import Union, Tuple
from datetime import datetime

from .DBConnection import DBConnection
from ..core.Exceptions import *

# fix ObjectId & FastApi conflict
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


class DBQueries:

    @classmethod
    def insert_to_database(cls, db_name:str, coll_name:str, data:dict)->Union[InsertOneResult, InsertManyResult]:
        """insert a single record or iterable of records to the database.

        Args:
            db_name (str): name of the database
            coll_name (str): name of the collection
            data (dict): data to be inserted

        Returns:
            An instance of class: pymongo.results.InsertOneResult or 
            pymongo.results.InsertManyResult
        """
        con = DBConnection.get_client()
        mydb = con[db_name]
        mycol = mydb[coll_name]

        if isinstance(data, list):
            return mycol.insert_many(data)
        else:
            return mycol.insert_one(data)

    @classmethod
    def count_all_documents(cls, db_name:str, coll_name:str)->int:
        """Count the number of documents in this collection.
        Args:
            db_name (str): name of the database
            coll_name (str): name of the collection

        Returns:
            int: number of documents in the collection        
        """
        con = DBConnection.get_client()

        mydb = con[db_name]
        mycol = mydb[coll_name]
        return mycol.count_documents({})

    @classmethod
    def fetch_last(cls, db_name:str, coll_name:str)->Cursor[_DocumentType]:
        """Fetch the last document in the collection.

        Args:
            db_name (str): name of the database
            coll_name (str): name of the collection

        Returns:
            Cursor[_DocumentType]: cursor to the last document in the collection
        """
        con = DBConnection.get_client()

        mydb = con[db_name]
        mycol = mydb[coll_name]

        return mycol.find().sort('_id', -1)[0]

    @classmethod
    def retrieve_documents(cls, db_name:str)->dict:
        """Retrieve all documents in the collection.
        Args:
            db_name (str): name of the database
            
        Returns:
            dict: all documents in the collection
        """
        con = DBConnection.get_client()
        mydb = con[db_name]
        response_data = {}
        response_data["data"] = {}

        for cols in mydb.list_collection_names():
            mycol = mydb[cols]
            li = [docs for docs in mycol.find({})]
            response_data["data"].update({mycol.full_name.split('.')[-1]: li})
        return response_data
     
    @classmethod
    def retrieve__id(cls, db_name:str, respondent_id:str, response_result:dict)->Tuple:
        """Retrieve the __id of via respondents_id
        Args:
            db_name (str): name of the database
            respondent_id (str): respondents_id of the family
            
        Returns:
            str: __id of the respondent"""
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
        try:
            return respli[0]['__id'], li[0]['volunteer_id'], li[0]['timestamp']
        except KeyError as e:
            return respli[0]['__id'], None, None
        
    @classmethod
    def retrieve_documents_by_id(cls, db_name:str,respondent_id:str, response_result:dict)->dict:
        """"Retrieve all documents in the collection by respondent_id.
        Args:
            db_name (str): name of the database
            respondent_id (str): respondent_id of the family
            response_result (dict): response result to be returned in case of error.

        Returns:
            dict: all documents in the collection by respondent_id
        """
        con = DBConnection.get_client()
        mydb = con[db_name]
        response_data = {}
        response_data["data"] = {}
        __id, volunteer_id, timestamp = cls.retrieve__id(db_name,respondent_id, response_result)
        for cols in mydb.list_collection_names():
            if cols=="meta":
                continue
            mycol = mydb[cols]
            li = [docs for docs in cls.filtered_db_search(db_name,cols,['__id','_id'],__id=__id)]
            response_data["data"].update({mycol.full_name.split('.')[-1]: li})
        response_data["data"].update({"filled_by": volunteer_id, "filled_time": timestamp})
        return response_data


    @classmethod
    def filtered_db_search(cls, db_name:str, coll_name:str,fields_to_drop:list ,**kwargs) -> pymongo.cursor.Cursor:
        """Search the database for a specific record.
        
        Args:
            db_name (str): name of the database
            coll_name (str): name of the collection
            fields_to_drop (list): list of fields to drop from the result
            **kwargs: key value pairs of the fields to search for
            
        Returns:
            pymongo.cursor.Cursor: cursor to the result of the search
        """
        con = DBConnection.get_client()

        mydb = con[db_name]
        mycol = mydb[coll_name]
        cursor = mycol.find(kwargs,{i:0 for i in fields_to_drop})

        return cursor

    @classmethod
    def fetch_indiv_document(cls,db_name:str,respondent_id:str, response_result:dict)->Cursor[_DocumentType]:
        """Fetch individual's documents in the collection.
        Args:
            db_name (str): name of the database
            respondent_id (str): respondent_id of the individual

        Returns:
            :class:Cursor[_DocumentType] individual's documents in the collection
        """
        indivdata = [docs for docs in cls.filtered_db_search(db_name,'fam_info',['__id','_id'],AADHAR_No=respondent_id)]
        if len(indivdata) == 0:
            raise InfoNotFoundException(response_result, "person with this id does not exist in the database")
        return indivdata[0]
    
    @classmethod
    def delete_database(cls,db_name:str)->None:
        """Delete the database.
        Args:
            db_name (str): name of the database
        """
        con = DBConnection.get_client()
        
        con.drop_database(db_name)

    @classmethod
    def list_database_names(cls)->list:

        """List all the database names.
        Returns:
            list: list of all database names
        """
        return [db_names for db_names in DBConnection.get_client().list_database_names() if
                            db_names not in ['Auth', 'string']]  

    @classmethod
    def create_db(cls,db_name,user_creds)->None:
        """Create a database.
        Args:
            dbname (str): name of the database
        """
        DBQueries.insert_to_database(db_name, coll_name="meta", data={'resp_id': user_creds.AADHAR,'volunteer_id': user_creds.AADHAR,'timestamp': datetime.now()})
                                                                 
