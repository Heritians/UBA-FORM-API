"""Wrapper functions for DBQueries module. These functions are used to perform 
CRUD operations on the database.
"""
from pymongo.results import InsertManyResult, InsertOneResult
from pymongo.cursor import Cursor
from pymongo.typings import _DocumentType

from typing import Union
from datetime import datetime

from ..models.RequestBodySchema import FormData
from ..utils.DBQueries import DBQueries
from ..utils.DBConnection import DBConnection
from ..core.Exceptions import *

collection_names = {
    "sv": "static_vars",
    # respondent's profile
    "rpf": "respondent_prof",
    # gen household info
    "ghi": "gen_ho_info",
    # family info
    "fi": "fam_info",
    # migration status
    "ms": "mig_status",
    # govt schemes
    "gs": "govt_schemes",
    # water source
    "ws": "water_source",
    # source of energy
    "soe": "source_of_energy",
    # land holding info
    "lhi": "land_holding_info",
    # agricultural inputs
    "ai": "agri_inputs",
    # agricultural products
    "ap": "agri_products",
    # livestock numbers
    "ln": "livestock_nos",
    # major problems
    "mp": "major_problems",
    # meta
    "meta": "meta"
}


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
    cursor = DBQueries.filtered_db_search(db, collection_names['meta'], [], resp_id=form_data.respondent_prof.id_no)

    if db in DBConnection.get_client().list_database_names() and len(list(cursor)) != 0:
        raise DuplicateEntryException(response_result)

    DBQueries.insert_to_database(form_data.static_vars.village_name,
                                 collection_names['meta'], dict({'resp_id': form_data.respondent_prof.id_no,
                                                                 'volunteer_id': user_AADHAR,
                                                                 'timestamp': datetime.now()})
                                 )
    fid = DBQueries.fetch_last(db, collection_names['meta'])['_id']

    # respondent's profile
    data = form_data.respondent_prof.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['rpf'], data)

    # gen_ho_data
    data = form_data.gen_ho_info.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ghi'], data)

    # fam_info
    data = form_data.fam_info
    data = [fam_mem_info.dict() for fam_mem_info in data]
    [indiv_info.update({"__id": fid}) for indiv_info in data]
    DBQueries.insert_to_database(db, collection_names['fi'], data)

    # migration info
    data = form_data.mig_status.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ms'], data)

    # gov schemes
    data = form_data.govt_schemes.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['gs'], data)

    # water source
    data = form_data.water_source.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ws'], data)

    # soucre of E
    data = form_data.source_of_energy.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['soe'], data)

    # Land holding info
    data = form_data.land_holding_info.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['lhi'], data)

    # agri inputs
    data = form_data.agri_inputs.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ai'], data)

    # agri products
    data = form_data.agri_products
    data = [agri_prods.dict() for agri_prods in data]
    [indiv_crop.update({"__id": fid}) for indiv_crop in data]
    DBQueries.insert_to_database(db, collection_names['ap'], data)

    # data['__id'] = fid
    # DBQueries.insert_to_database(db, collection_names['ap'], data)

    # livestock nums
    data = form_data.livestock_nos.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ln'], data)

    # major probs
    data = form_data.major_problems.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['mp'], data)

    response_result['status'] = 'success'
    response_result['message'][0] = 'authenticated'
    response_result['message'].append('posted successfully')


def fetch_from_db(response_result: dict, resp_data: str)->dict:
    """Wrapper function to fetch data from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        resp_data (str): data to be fetched from the database.
        
    Returns:
        A dictionary containing the data fetched from the database.
    """
    db = resp_data
    result = DBQueries.retrieve_documents(db)
    return result


def fetch_familydata(response_result: dict, resp_data: str, respondent_id: str)->dict:
    """Wrapper function to fetch family data from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        resp_data (str): data to be fetched from the database.
        
    Returns:
        A dictionary containing the data of the family fetched from the database.
    """
    db = resp_data
    result = DBQueries.retrieve_documents_by_id(db, respondent_id, response_result)
    return result


def fetch_individualdata(response_result: dict, db_name: str, respondent_id: str)->Cursor[_DocumentType]:
    """Wrapper function to fetch individual data from the database.
    Args:
        response_result (dict): response result to be returned in case of error.
        db_name (str): name of the database.
        respondent_id (str): id of the respondent.
        
    Returns:
        Cursor[_DocumentType]: A cursor containing the data of the individual 
        fetched from the database."""
    result = DBQueries.fetch_indiv_document(db_name, respondent_id, response_result)
    return result


def get_db_conn_flag()->DBConnection:
    """Wrapper function to get the database connection flag.
    Returns:
        DBConnection: An instance of class: DBConnection.
    """
    return DBConnection.flag
