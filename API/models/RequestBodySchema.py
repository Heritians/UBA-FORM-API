from pydantic import BaseModel

from typing import Union, Tuple, List


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
    name: str
    age: int
    sex: str
    marital_status: str
    education: str
    schooling_status: str
    AADHAR_No: str
    has_bank_acc: bool
    is_computer_literate: bool
    has_SSP: bool
    health_prob: Union[str,None]
    has_MNREGA: bool
    SHG: bool
    occupations: str


class _4_MigrationStatusFamily(BaseModel):
    are_migrants: bool
    num_migrants: int
    migration_period_months: float
    years_since_migration: float

class _5_GovernmentSchemes(BaseModel):
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

class _6_WaterSource(BaseModel):
    piped_water:Tuple[bool,int]
    hand_pump:Tuple[bool,int]
    comm_water:Tuple[bool,int]
    open_well:Tuple[bool,int]
    mode_of_water_storage:str
    other_water_source:str

class _7_1_ApplianceUsage(BaseModel):
    appliance_name:str
    appliance_nos:int
    appliance_dur:int

class _7_SourceOfEnergy(BaseModel):
    electricity_conn:bool
    elec_avail_perday_hour:int
    lighting:Union[Tuple[str], List[str]]
    cooking:Union[Tuple[str], List[str]]
    cook_chullah:str
    appliances:Union[List[_7_1_ApplianceUsage],Tuple[_7_1_ApplianceUsage]]

class _8_LandholdingInformationAcres(BaseModel):
    total_land:float
    irrigated_area:float
    barren_or_wasteland:float
    cultivable_area:float
    unirrigated_area:float
    uncultivable_area:float

class _9_AgriculturalInputs(BaseModel):
    is_chemical_fertilizer_used:Tuple[bool,float]
    is_chemical_insecticide_used:Tuple[bool,float]
    is_chemical_weedice_used:Tuple[bool,float]
    is_chemical_organic_manuevers:Tuple[bool,float]
    irrigation:str
    irrigation_sys:str

class _10_AgriculturalProductsNormalYear(BaseModel):
    crop_name:str
    crop_area_prev_yr_acre:float
    productivity_in_quintals_per_acre:float

class _11_LivestockNumbers(BaseModel):
    cows:int
    buffalo:int
    goats_and_sheeps:int
    calves:int
    bullocks:int
    poultry_and_ducks:int
    livestock_shelter:Union[List[str],Tuple[str]]
    avg_daily_milk_prod_litres:float
    animal_waste_or_cow_dung_kgs:float

class _12_MajorProblems(BaseModel):
    problems:Union[List[str],Tuple[str]]
    Suggestions_by_villagers:Union[List[str],Tuple[str]]


class FormData(BaseModel):
    # form details
    static_vars: _0_FormDetails

    # respondent's profile
    respondent_prof: _1_respondent_profile

    # gen household info
    gen_ho_info: _2_GeneralHouseHoldInformation

    # family info
    fam_info: Union[List[_3_FamilyInformation], Tuple[_3_FamilyInformation]]

    #migration status
    mig_status: _4_MigrationStatusFamily

    # govt schemes
    govt_schemes: _5_GovernmentSchemes

    # water source
    water_source: _6_WaterSource

    # source of energy
    source_of_energy: _7_SourceOfEnergy

    # land holding info
    land_holding_info: _8_LandholdingInformationAcres

    # agricultural inputs
    agri_inputs: _9_AgriculturalInputs

    # agricultural products
    agri_products: Union[List[_10_AgriculturalProductsNormalYear], Tuple[_10_AgriculturalProductsNormalYear]]

    # livestock numbers
    livestock_nos: _11_LivestockNumbers

    # major problems
    major_problems: _12_MajorProblems
