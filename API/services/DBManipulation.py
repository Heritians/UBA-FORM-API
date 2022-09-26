from ..RequestBodySchema import FormData
from ..utils.DBQueries import DBQueries


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


def commit_to_db(response_result: dict, form_data: FormData):
    db = form_data.static_vars.village_name
    DBQueries.insert_to_database(form_data.static_vars.village_name,
                                 collection_names['meta'], dict({'resp_id': form_data.respondent_prof.id_no})
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
    data = form_data.agri_products.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ap'], data)

    # livestock nums
    data = form_data.livestock_nos.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['ln'], data)

    # major probs
    data = form_data.major_problems.dict()
    data['__id'] = fid
    DBQueries.insert_to_database(db, collection_names['mp'], data)

    response_result['status'] = 'success'


def fetch_from_db(response_result: dict,resp_data:str):
    db = resp_data
    result=DBQueries.retrieve_documents(db)
    return result


    