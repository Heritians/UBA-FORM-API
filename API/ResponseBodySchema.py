from pydantic import BaseModel

from typing import Union, Tuple, List

from .RequestBodySchema import (_4_MigrationStatusFamily,_5_GovernmentSchemes,_7_1_ApplianceUsage,_8_LandholdingInformationAcres,_9_AgriculturalInputs,_10_AgriculturalProductsNormalYear,_11_LivestockNumbers,_12_MajorProblems)

class _2_GeneralHouseHoldInformation(BaseModel):
    ho_id: str
    hoh_gender: str
    category: str
    pov_status: str
    house_type: str
    toilet: str
    drainage_status: str
    waste_collection_sys: str
    compost_pit: str
    biogas_plant: str
    annual_income: float  

#fam info to be discussed

class _6_WaterSource(BaseModel):
    piped_water:Tuple[bool,int]
    hand_pump:Tuple[bool,int]
    comm_water:Tuple[bool,int]
    open_well:Tuple[bool,int]  

class _7_SourceOfEnergy(BaseModel):
    electricity_conn:bool
    elec_avail_perday_hour:int
    lighting:Union[Tuple[str], List[str]]
    cooking:Union[Tuple[str], List[str]]
    appliances:Union[List[_7_1_ApplianceUsage],Tuple[_7_1_ApplianceUsage]]                

class EDAResponseData(BaseModel):
    # gen household info
    gen_ho_info:  _2_GeneralHouseHoldInformation

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
    agri_products: _10_AgriculturalProductsNormalYear

    # livestock numbers
    livestock_nos: _11_LivestockNumbers

    # major problems
    major_problems: _12_MajorProblems    