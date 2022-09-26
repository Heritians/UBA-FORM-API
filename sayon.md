    # gen household info
_2_GeneralHouseHoldInformation:
ho_id:int
gender:str 
categrory:str (0,1,2 one hot maybe..lets see)
pov_stat:str
type_of_house:str 
toilet:str
drainage:str
waste_coll:str
compost:str
biogas:str


    # family info (to be discussed)
Union[List[_3_FamilyInformation], Tuple[_3_FamilyInformation]]

    #migration status
_4_MigrationStatusFamily
mig_for_work:bool
mig_members:int
duration:int
years:int


    # govt schemes
_5_GovernmentSchemes
sum of schemes

    # water source
_6_WaterSource (to be discussed)
piped_water:bool
comm_h2o:bool
hand:bool
open_welll:bool

    # source of energy
_7_SourceOfEnergy
has_ho_elec:bool
elc_avail/day:float
lighting:str
appliances: (to be discussed but chahiye)


    # land holding info
_8_LandholdingInformationAcres
all_cols:float



    # agricultural inputs
_9_AgriculturalInputs
chem_fert:bool,float
chem_ins:bool,float
chem_weed:bool,float
org_man:bool,float
irri:str
irri_sys:str

    # agricultural products
_10_AgriculturalProductsNormalYear
crop:str
area:float
prod:float

    # livestock numbers
_11_LivestockNumbers
cows:int
buff:int
sheep:int
bull:int
duck:int
shelter:str
avg_daily_prod:float
animal_waste:float

    # major problems
_12_MajorProblems
problems:str
suggestions:str

