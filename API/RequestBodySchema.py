from pydantic import BaseModel

from typing import Union, Tuple, List
from typing_extensions import TypedDict


class FormData(BaseModel):
    # form details
    static_vars: TypedDict = {
        'village_name': str,
        'grampanchyat_name': str,
        'ward_no': str,
        'block': str,
        'district': str,
        'state': str,
    }

    # respondent's profile
    respondent_prof: TypedDict = {
        'respondents_name': str,
        'respondents_age': int,
        'relation_w_hoh': str,
        'respondents_contact': str,
        'id_type': str,
        'id_no': str,
    }

    # gen household info
    gen_ho_info: TypedDict = {
        'ho_id': str,
        'hoh_name': str,
        'hoh_gender': str,
        'category': str,
        'pov_status': str,
        'own_house': bool,
        'house_type': str,
        'toilet': str,
        'drainage_status': str,
        'waste_collection_sys': str,
        'compost_pit': str,
        'biogas_plant': str,
        'annual_income': float,
    }

    # family info
    fam_info: TypedDict = {
        'name': Union[Tuple[str], List[str]],
        'age': Union[Tuple[int], List[int]],
        'sex': Union[Tuple[str], List[str]],
        'martial_status': Union[Tuple[str], List[str]],
        'education': Union[Tuple[str], List[str]],
        'schooling_status': Union[Tuple[str], List[str]],
        'has_AADHAR': Union[Tuple[bool], List[bool]],
        'has_bank_acc': Union[Tuple[bool], List[bool]],
        'is_computer_literate': Union[Tuple[bool], List[bool]],
        'has_SSP': Union[Tuple[bool], List[bool]],
        'health_prob': Union[Union[Tuple[str], List[str], None]],
        'has_MNREGA': Union[Tuple[bool], List[bool]],
        'SHG': Union[Tuple[bool], List[bool]],
        'Occupations': Union[Tuple[str], List[str]],
    }


class Test(BaseModel):
    name: str
