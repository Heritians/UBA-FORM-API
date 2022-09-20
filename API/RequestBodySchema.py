from pydantic import BaseModel

from typing import Union, Tuple, List
from typing_extensions import TypedDict


class _0_FormDetails(BaseModel):
    village_name: str
    grampanchyat_name: str
    ward_no: str
    block: str
    district: str
    state: str


class _1_respondent_profile(BaseModel):
    respondents_name: str
    respondents_age: int
    relation_w_hoh: str
    respondents_contact: str
    id_type: str
    id_no: str


class _2_GeneralHouseHoldInformation(BaseModel):
    ho_id: str
    hoh_name: str
    hoh_gender: str
    category: str
    pov_status: str
    own_house: bool
    house_type: str
    toilet: str
    drainage_status: str
    waste_collection_sys: str
    compost_pit: str
    biogas_plant: str
    annual_income: float


class _3_FamilyInformation(BaseModel):
    name: Union[Tuple[str], List[str]]
    age: Union[Tuple[int], List[int]]
    sex: Union[Tuple[str], List[str]]
    martial_status: Union[Tuple[str], List[str]]
    education: Union[Tuple[str], List[str]]
    schooling_status: Union[Tuple[str], List[str]]
    has_AADHAR: Union[Tuple[bool], List[bool]]
    has_bank_acc: Union[Tuple[bool], List[bool]]
    is_computer_literate: Union[Tuple[bool], List[bool]]
    has_SSP: Union[Tuple[bool], List[bool]]
    health_prob: Union[Union[Tuple[str], List[str]],None]
    has_MNREGA: Union[Tuple[bool], List[bool]]
    SHG: Union[Tuple[bool], List[bool]]
    occupations: Union[Tuple[str], List[str]]


class _4_MigrationStatusFamily(BaseModel):
    are_migrants: bool
    num_migrants: int
    migration_period_months: float
    years_since_migration: float


class FormData(BaseModel):
    # form details
    static_vars: _0_FormDetails

    # respondent's profile
    respondent_prof: _1_respondent_profile

    # gen household info
    gen_ho_info: _2_GeneralHouseHoldInformation

    # family info
    fam_info: _3_FamilyInformation
