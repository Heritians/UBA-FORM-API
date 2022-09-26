import unittest


class MyTestCase(unittest.TestCase):
    def test_post2db(self):
        import requests

        data = {
  "static_vars": {
    "village_name": "string",
    "grampanchyat_name": "string",
    "ward_no": "string",
    "block": "string",
    "district": "string",
    "state": "string"
  },
  "respondent_prof": {
    "respondents_name": "string",
    "respondents_age": 0,
    "relation_w_hoh": "string",
    "respondents_contact": "string",
    "id_type": "string",
    "id_no": "212121"
  },
  "gen_ho_info": {
    "ho_id": "string",
    "hoh_name": "string",
    "hoh_gender": "string",
    "category": "string",
    "pov_status": "string",
    "own_house": True,
    "house_type": "string",
    "toilet": "string",
    "drainage_status": "string",
    "waste_collection_sys": "string",
    "compost_pit": "string",
    "biogas_plant": "string",
    "annual_income": 0
  },
  "fam_info": [
    {
      "name": "string",
      "age": 0,
      "sex": "string",
      "martial_status": "string",
      "education": "string",
      "schooling_status": "string",
      "has_AADHAR": True,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "string",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "string"
    },
    {
      "name": "hemanth",
      "age": 19,
      "sex": "male",
      "martial_status": "string",
      "education": "string",
      "schooling_status": "string",
      "has_AADHAR": True,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "string",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "string"
    },
    {
      "name": "Mayuresh",
      "age": 19,
      "sex": "male",
      "martial_status": "string",
      "education": "string",
      "schooling_status": "string",
      "has_AADHAR": True,
      "has_bank_acc": True,
      "is_computer_literate": True,
      "has_SSP": True,
      "health_prob": "string",
      "has_MNREGA": True,
      "SHG": True,
      "occupations": "string"
    }

  ],
  "mig_status": {
    "are_migrants": True,
    "num_migrants": 0,
    "migration_period_months": 0,
    "years_since_migration": 0
  },
  "govt_schemes": {
    "PM_jan_dhan_yojana": 0,
    "PM_ujjawala_yojana": 0,
    "PM_awas_yojana": 0,
    "sukanya_samriddhi_yojana": 0,
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
      0, 0
    ],
    "hand_pump": [
      0, 0
    ],
    "comm_water": [
      0, 0
    ],
    "open_well": [
      0, 0
    ],
    "mode_of_water_storage": "string",
    "other_water_source": "string"
  },
  "source_of_energy": {
    "electricity_conn": True,
    "elec_avail_perday_hour": 0,
    "lighting": [
      "string"
    ],
    "cooking": [
      "string"
    ],
    "cook_chullah": "string",
    "appliances": [
      {
        "appliance_name": "string",
        "appliance_nos": 0,
        "appliance_dur": 0
      }
    ]
  },
  "land_holding_info": {
    "total_land": 0,
    "irrigated_area": 0,
    "barren_or_wasteland": 0,
    "cultivable_area": 0,
    "unirrigated_area": 0,
    "uncultivable_area": 0
  },
  "agri_inputs": {
    "is_chemical_fertilizer_used": [
      0, 0
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
    "irrigation": [
      0, 0
    ]
  },
  "agri_products": {
    "crop_name": "string",
    "crop_area_prev_yr_acre": 0,
    "productivity_in_quintals_per_acre": 0
  },
  "livestock_nos": {
    "cows": 0,
    "buffalo": 0,
    "goats_and_sheeps": 0,
    "calves": 0,
    "bullocks": 0,
    "poultry_and_ducks": 0,
    "livestock_shelter": [
      "string"
    ],
    "avg_daily_milk_prod_litres": 0,
    "animal_waste_or_cow_dung_kgs": 0
  },
  "major_problems": {
    "problems": [
      "string"
    ],
    "Suggestions_by_villagers": [
      "string"
    ]
  }
}
        url = "http://localhost:8000/api/post_data"
        response = requests.post(url, json=data)
        print(response.text)
        self.assertEqual(response.text, "200")  # add assertion here


if __name__ == '__main__':
    unittest.main()
