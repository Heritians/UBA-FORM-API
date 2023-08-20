"""Wrapper functions for DBQueries module. These functions are used to perform 
CRUD operations on the database.
"""
from typing import Union, Callable
from datetime import datetime

from pymongo.results import InsertManyResult, InsertOneResult
from pymongo.cursor import Cursor
from pymongo.typings import _DocumentType

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from API.models import FormData
from API.utils.DBConnection import DBConnection
from API.core.Exceptions import *

from .utils import DBQueries, field_manager

collection_names = {
    # family data
    "fam_data":"family_data",
}

def json_encoder(custom_encodings: dict):
    """Wrapper function to encode the data to JSON format.
    
    Args:
        custom_encodings (dict): custom encodings to be used while encoding the data.
    
    Returns:
        A function which encodes the data to desired JSON format.
    """
    def wrapper(func: Callable):
        def custom_json_encoder(*args, **kwargs):
            return jsonable_encoder(func(*args, **kwargs), custom_encoder=custom_encodings)
        return custom_json_encoder
    return wrapper

def commit_to_db(response_result: dict, form_data: FormData, user_AADHAR: str)->Union[InsertOneResult,InsertManyResult]:
    """Wrapper function to commit the data to the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        form_data (FormData): data to be committed to the database.
        user_AADHAR (str): Aadhar Number of the volunteer/user filling the form.
        
    Returns:
        An instance of class: pymongo.results.InsertOneResult or 
        pymongo.results.InsertManyResult which returns the result of the commit operation.
    """
    db = form_data.static_vars.village_name
    cursor = DBQueries.filtered_db_search(db, collection_names['fam_data'], [], search_idxs={"respondent_prof.id_no":form_data.respondent_prof.id_no})

    if db in DBConnection.get_client().list_database_names() and len(list(cursor)) != 0:
        raise DuplicateEntryException(response_result)
    
    data=form_data.model_dump()
    data.update({"volunteer_id": user_AADHAR, "timestamp": datetime.now()})
    data.pop("static_vars")
    DBQueries.insert_to_database(db, collection_names['fam_data'], data)

    response_result['status'] = 'success'
    response_result['message'][0] = 'authenticated'
    response_result['message'].append('posted successfully')

@json_encoder({ObjectId: str})
def fetch_from_db(response_result: dict, resp_data: str)->dict:
    """Wrapper function to fetch data from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        resp_data (str): data to be fetched from the database.
        
    Returns:
        A dictionary containing the data fetched from the database.
    """
    db = resp_data
    result = DBQueries.retrieve_documents(db,collection_names["fam_data"])
    return result


def fetch_familydata(response_result: dict, village_name: str, respondent_id: str)->dict:
    """Wrapper function to fetch family data from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        resp_data (str): data to be fetched from the database.
        
    Returns:
        A dictionary containing the data of the family fetched from the database.
    """
    db = village_name
    doc = [docs for docs in DBQueries.filtered_db_search(db,collection_names["fam_data"],[],search_idxs={"respondent_prof.id_no":respondent_id})]

    if len(doc) == 0:
        raise InfoNotFoundException(response_result,"family with this respondent id does not exist in the database")
    return doc[0]

def fetch_individualdata(response_result: dict, db_name: str, AADHAR_No: str)->Cursor[_DocumentType]:
    """Wrapper function to fetch individual data from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        db_name (str): name of the database.
        AADHAR_No (str): id of the respondent.
        
    Returns:
        Cursor[_DocumentType]: A cursor containing the data of the individual 
        fetched from the database.
    """
    exclude_fields = field_manager.get_form_fields(FormData, exclude=["fam_info"])
    exclude_fields += ["_id","timestamp","volunteer_id"]
    indivdata = [docs for docs in DBQueries.filtered_db_search(db_name,collection_names["fam_data"],exclude_fields,search_idxs={"fam_info.AADHAR_No":AADHAR_No})]
    if len(indivdata) == 0:
        raise InfoNotFoundException(response_result, "person with this id does not exist in the database")
    
    fam_members = [doc for doc in indivdata[0]["fam_info"] if doc["AADHAR_No"] == AADHAR_No]

    return fam_members[0]


def get_db_conn_flag()->DBConnection:
    """Wrapper function to get the database connection flag.
    Returns:
        DBConnection: An instance of class: DBConnection.
    """
    return DBConnection.flag

def delete_village_data(village_name: str,response_result:FrontendResponseModel)->None:
    """Wrapper function to delete the data of a village from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        village_name (str): name of the village whose data is to be deleted.
        
    Returns:
        A dictionary containing the data of the family fetched from the database.
    """
    result = DBQueries.delete_database(village_name)
    response_result['status'] = 'success'
    response_result['message'] = ['Authenticated','Village name removed']
    return result

def get_available_villages(response_result:FrontendResponseModel)->list:
    """Wrapper function to get the list of villages in the database.
    Returns:
        list: A list containing the names of the villages in the database.
    """
    response_result['status'] = 'success'
    return DBQueries.list_database_names()


def create_new_village(dbname, user_creds, response_result:FrontendResponseModel)->None:
    """Wrapper function to create a new village in the database.
    """
    village_list=get_available_villages(response_result)
    if dbname in village_list:
        raise DuplicateVillageException(response_result)
    DBQueries.create_db(dbname,user_creds)
    response_result['status'] = 'success'
    response_result['message'] = ['Authenticated','Village name added']
    response_result["data"]={}

@json_encoder({ObjectId: str})
def get_resp_data_on_date(dbname, date, response_result:FrontendResponseModel)->list:
    """Wrapper function to get the data of users who have filled the form on a given date.
    """
    start_date=datetime.strptime(f"{date} 00:00:00","%Y-%m-%d %H:%M:%S")
    end_date=datetime.strptime(f"{date} 23:59:59","%Y-%m-%d %H:%M:%S")

    cursor=DBQueries.filtered_db_search(dbname,collection_names["fam_data"],[],
                                        search_idx={"timestamp":{"$gte":start_date,"$lte":end_date}})

    resp_data=[doc for doc in cursor]

    response_result['status'] = 'success'
    response_result['message'] = ['Authenticated']

    return resp_data