import requests

def get_access_token(data):
    url = "http://127.0.0.1:8000/login"
    headers={
        "accept":"application/json",
   } 
    response = requests.post(url, params=data,headers=headers)
    access_token=response.json()['access_token']
    return access_token

def query_get(url,headers,data):
    response = requests.get(url, params=data,headers=headers)
    return response

def query_post(url,headers,data):
    response = requests.post(url, data=data,headers=headers)
    return response
data={
  "static_vars": {
    "village_name": "Sehore",
    "grampanchyat_name": "bhairaghad",
    "ward_no": "7",
    "block": "141",
    "district": "kothri-kalan",
    "state": "Madhya Pradesh"
  },
  "respondent_prof": {
    "respondents_name": "Hemanth",
    "respondents_age": 20,
    "relation_w_hoh": "Son",
    "respondents_contact": "8479239724",
    "id_type": "AC",
    "id_no": "8523705708935799"
  },
  "gen_ho_info": {
    "ho_id": "A1",
    "hoh_name": "Dada",
    "hoh_gender": "Male",
    "category": "OBC",
    "pov_status": "BPL",
    "own_house": True,
    "house_type": "pucca",
    "toilet": "Private",
    "drainage_status": "open",
    "waste_collection_sys": "doorstep",
    "compost_pit": "Individual",
    "biogas_plant": "Group",
    "annual_income": 120000
  },
  "fam_info": [
    {
      "name": "Mayuresh",
      "age": 20,
      "sex": "Male",
      "martial_status": "U",
      "education": "College",
      "schooling_status": "3 year",
      "AADHAR_No": 1234,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "None",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "Student"
    },
    {
      "name": "Anmol",
      "age": 20,
      "sex": "Male",
      "martial_status": "U",
      "education": "College",
      "schooling_status": "3 year",
      "AADHAR_No": 2345,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "None",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "Student"
    },
  {
      "name": "Hemanth",
      "age": 20,
      "sex": "Male",
      "martial_status": "U",
      "education": "College",
      "schooling_status": "3 year",
      "AADHAR_No": 3456,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "None",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "Student"
    },
    {
      "name": "Gargi",
      "age": 20,
      "sex": "Female",
      "martial_status": "U",
      "education": "College",
      "schooling_status": "3 year",
      "AADHAR_No": 4567,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "None",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "Student"
    }
 ],
  "mig_status": {
    "are_migrants": False,
    "num_migrants": 0,
    "migration_period_months": 0,
    "years_since_migration": 0
  },
  "govt_schemes": {
    "PM_jan_dhan_yojana": 2,
    "PM_ujjawala_yojana": 3,
    "PM_awas_yojana": 2,
    "sukanya_samriddhi_yojana": 3,
    "mudra_yojana": 0,
    "PM_jivan_jyoti_yojana": 0,
    "PM_suraksha_bima_yojana": 0,
    "atal_pension_yojana": 0,
    "fasal_bima_yojana": 0,
    "kaushal_vikas_yojana": 0,
    "krishi_sinchai_yojana": 0,
    "jan_aushadhi_yojana": 0,
    "SBM_toilet": 0,
    "soil_health_card": 0,
    "ladli_lakshmi_yojana": 0,
    "janni_suraksha_yojana": 0,
    "kisan_credit_card": 0
  },
  "water_source": {
    "piped_water": [
      True, 10
    ],
    "hand_pump": [
      True, 20
    ],
    "comm_water": [
      False, 0
    ],
    "open_well": [
      True, 40
    ],
    "mode_of_water_storage": "individual",
    "other_water_source": "None"
  },
  "source_of_energy": {
    "electricity_conn": True,
    "elec_avail_perday_hour": 12,
    "lighting": [
      "electricity"
    ],
    "cooking": [
      "LPG"
    ],
    "cook_chullah": "Smokeless",
    "appliances": [
      {
        "appliance_name": "fan",
        "appliance_nos": 2,
        "appliance_dur": 5
      },
      {
        "appliance_name": "bulb",
        "appliance_nos": 2,
        "appliance_dur": 5
      }
    ]
  },
  "land_holding_info": {
    "total_land": 2,
    "irrigated_area": 0.5,
    "barren_or_wasteland": 0.1,
    "cultivable_area": 0.4,
    "unirrigated_area": 0.3,
    "uncultivable_area": 0.2
  },
  "agri_inputs": {
    "is_chemical_fertilizer_used": [
      1, 5
    ],
    "is_chemical_insecticide_used": [
      0, 0
    ],
    "is_chemical_weedice_used": [
      0, 0
    ],
    "is_chemical_organic_manuevers": [
      0, 0
    ],
    "irrigation":"Open",
    "irrigation_sys":"Open"
  },
  "agri_products": {
    "crop_name": "rice",
    "crop_area_prev_yr_acre": 0.2,
    "productivity_in_quintals_per_acre": 3
  },
  "livestock_nos": {
    "cows": 2,
    "buffalo": 2,
    "goats_and_sheeps": 0,
    "calves": 1,
    "bullocks": 1,
    "poultry_and_ducks": 0,
    "livestock_shelter": [  
      "open"
    ],
    "avg_daily_milk_prod_litres": 5,
    "animal_waste_or_cow_dung_kgs": 1
  },
  "major_problems": {
    "problems": [
      "None"
    ],
    "Suggestions_by_villagers": [
      "None"
    ]
  }
}
BASE_URL = "https://ubaformapi-b79iq4w6b-fastapis-build.vercel.app"
