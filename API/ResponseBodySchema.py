from pydantic import BaseModel

from typing import Union, Tuple, List
from bson.objectid import ObjectId


class _0_FormDetails(BaseModel):
    _id:ObjectId
    village_name: str
    grampanchyat_name: str
    ward_no: str
    block: str
    district: str
    state: str
    __id:ObjectId



class _1_respondent_profile(BaseModel):
    _id:ObjectId
    respondents_name: str
    respondents_age: int
    relation_w_hoh: str
    respondents_contact: str
    id_type: str
    id_no: str
    __id:ObjectId


class _2_GeneralHouseHoldInformation(BaseModel):
    _id:ObjectId
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
    __id:ObjectId


class _3_FamilyInformation(BaseModel):
    _id:ObjectId
    name: str
    age: int
    sex: str
    martial_status: str
    education: str
    schooling_status: str
    has_AADHAR: bool
    has_bank_acc: bool
    is_computer_literate: bool
    has_SSP: bool
    health_prob: Union[str,None]
    has_MNREGA: bool
    SHG: bool
    occupations: str
    __id:ObjectId


class _4_MigrationStatusFamily(BaseModel):
    _id:ObjectId
    are_migrants: bool
    num_migrants: int
    migration_period_months: float
    years_since_migration: float
    __id:ObjectId

class _5_GovernmentSchemes(BaseModel):
    _id:ObjectId
    PM_jan_dhan_yojana: int
    PM_ujjawala_yojana: int
    PM_awas_yojana: int
    sukanya_samriddhi_yojana: int
    mudra_yojana: int
    PM_jivan_jyoti_yojana: int
    PM_suraksha_bima_yojana: int
    atal_pension_yojana: int
    fasal_bima_yojana: int
    kaushal_vikas_yojana: int
    krishi_sinchai_yojana: int
    jan_aushadhi_yojana: int
    SBM_toilet: int
    soil_health_card: int
    ladli_lakshmi_yojana: int
    janni_suraksha_yojana: int
    kisan_credit_card: int
    __id:ObjectId

class _6_WaterSource(BaseModel):
    _id:ObjectId
    piped_water:Tuple[bool,int]
    hand_pump:Tuple[bool,int]
    comm_water:Tuple[bool,int]
    open_well:Tuple[bool,int]
    mode_of_water_storage:str
    other_water_source:str
    __id:ObjectId

class _7_1_ApplianceUsage(BaseModel):
    appliance_name:str
    appliance_nos:int
    appliance_dur:int
class _7_SourceOfEnergy(BaseModel):
    _id:ObjectId
    electricity_conn:bool
    elec_avail_perday_hour:int
    lighting:Union[Tuple[str], List[str]]
    cooking:Union[Tuple[str], List[str]]
    cook_chullah:str
    appliances:Union[List[_7_1_ApplianceUsage],Tuple[_7_1_ApplianceUsage]]
    __id:ObjectId

class _8_LandholdingInformationAcres(BaseModel):
    _id:ObjectId
    total_land:float
    irrigated_area:float
    barren_or_wasteland:float
    cultivable_area:float
    unirrigated_area:float
    uncultivable_area:float
    __id:ObjectId

class _9_AgriculturalInputs(BaseModel):
    _id:ObjectId
    is_chemical_fertilizer_used:Tuple[bool,float]
    is_chemical_insecticide_used:Tuple[bool,float]
    is_chemical_weedice_used:Tuple[bool,float]
    is_chemical_organic_manuevers:Tuple[bool,float]
    irrigation:Tuple[bool,float]
    irrigation:Tuple[bool,float]
    __id:ObjectId

class _10_AgriculturalProductsNormalYear(BaseModel):
    _id:ObjectId
    crop_name:str
    crop_area_prev_yr_acre:float
    productivity_in_quintals_per_acre:float
    __id:ObjectId

class _11_LivestockNumbers(BaseModel):
    _id:ObjectId
    cows:int
    buffalo:int
    goats_and_sheeps:int
    calves:int
    bullocks:int
    poultry_and_ducks:int
    livestock_shelter:Union[List[str],Tuple[str]]
    avg_daily_milk_prod_litres:float
    animal_waste_or_cow_dung_kgs:float
    __id:ObjectId

class _12_MajorProblems(BaseModel):
    _id:ObjectId
    problems:Union[List[str],Tuple[str]]
    Suggestions_by_villagers:Union[List[str],Tuple[str]]
    __id:ObjectId


class EDAResponseData(BaseModel):
    # form details
    # static_vars: Union[List[_0_FormDetails],Tuple[_0_FormDetails]]

    # respondent's profile
    respondent_prof: Union[List[_1_respondent_profile],Tuple[_1_respondent_profile]]

    # gen household info
    gen_ho_info: Union[List[_2_GeneralHouseHoldInformation],Tuple[_2_GeneralHouseHoldInformation]]

    # family info
    fam_info: Union[List[_3_FamilyInformation], Tuple[_3_FamilyInformation]]

    #migration status
    mig_status: Union[List[_4_MigrationStatusFamily],Tuple[_4_MigrationStatusFamily]]

    # govt schemes
    govt_schemes: Union[List[_5_GovernmentSchemes],Tuple[_5_GovernmentSchemes]]

    # water source
    water_source: Union[List[_6_WaterSource],Tuple[_6_WaterSource]]

    # source of energy
    source_of_energy: Union[List[_7_SourceOfEnergy],Tuple[_7_SourceOfEnergy]]

    # land holding info
    land_holding_info: Union[List[_8_LandholdingInformationAcres],Tuple[_8_LandholdingInformationAcres]]

    # agricultural inputs
    agri_inputs: Union[List[_9_AgriculturalInputs],Tuple[_9_AgriculturalInputs]]

    # agricultural products
    agri_products: Union[List[_10_AgriculturalProductsNormalYear],Tuple[_10_AgriculturalProductsNormalYear]]

    # livestock numbers
    livestock_nos: Union[List[_11_LivestockNumbers],Tuple[_11_LivestockNumbers]]

    # major problems
    major_problems: Union[List[_12_MajorProblems],Tuple[_12_MajorProblems]]            

