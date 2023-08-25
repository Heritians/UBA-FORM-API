""" Queries script for the API. It is used to create the queries 
that are used to interact with the database. 
"""
import regex as re
from typing import Union, Tuple, List
from datetime import datetime

import pymongo.cursor
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult,InsertManyResult
from pymongo.typings import _DocumentType

from API.utils.DBConnection import DBConnection
from API.core.Exceptions import *


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
    def retrieve_documents(cls, db_name:str, coll_name:str)->dict:
        """Retrieve all documents in the collection.
        Args:
            db_name (str): name of the database
            
        Returns:
            dict: all documents in the collection
        """
        con = DBConnection.get_client()
        mydb = con[db_name]

        mycol = mydb[coll_name]
        return {"data":[docs for docs in mycol.find({})]}
    

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

        search_idxs = {}
        for key, val in kwargs.items():
            if isinstance(val, dict):
                search_idxs.update({nested_key:nested_val for nested_key, nested_val in val.items()})
            else:
                search_idxs.update({key:val})    
        
        cursor = mycol.find(search_idxs ,{i:0 for i in fields_to_drop})

        return cursor
    

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
                            not (db_names == 'Auth' or db_names.startswith('test'))]  

    @classmethod
    def create_db(cls, db_name:str, user_creds:str)->None:
        """Create a database.
        Args:
            dbname (str): name of the database
        """
        DBQueries.insert_to_database(db_name, coll_name="family_data", data={'resp_id': user_creds.AADHAR,'volunteer_id': user_creds.AADHAR,'timestamp': datetime.now()})
                                                                 
