from ..RequestBodySchema import FormData
from ..utils.DBQueries import DBQueries


def commit_to_db(response_result: dict, form_data: FormData):
        # data = [fam_mem_info.dict() for fam_mem_info in form_data.fam_info]

        DBQueries.insert_to_database('UBA_FORM_DB', 'fam_info', form_data.water_source.dict())
        response_result['status'] = 'success'
