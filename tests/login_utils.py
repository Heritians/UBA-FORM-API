import json

import requests
from dotenv import load_dotenv
load_dotenv()

# BASE_URL = "https://ubaformapi-git-prod-fastapis-build.vercel.app" # for GitHub actions
# BASE_URL = "http://127.0.0.1:8000" # for testing locally
BASE_URL = "https://ubaformapi-hzekeban1-fastapis-build.vercel.app"

def get_access_token(data, return_refresh_token=False):
    url = BASE_URL + "/auth/login"
    headers = {
        "accept": "application/json",
    }
    response = requests.post(url, params=data, headers=headers)
    access_token = response.json()['access_token']
    if return_refresh_token:
        refresh_token = response.json()['refresh_token']
        return access_token, refresh_token
    return access_token


def query_get(url, headers, data):
    response = requests.get(url, params=data, headers=headers)
    return response


def query_post(url, headers, data):
    response = requests.post(url, data=data, headers=headers)
    return response


with open("./intended_responses/postdata.json", 'r') as f:
    data = json.load(f)
