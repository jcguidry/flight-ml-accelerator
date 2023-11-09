import requests
import json
from datetime import datetime as dt
from typing import Dict, Any

class FlightAwareAPI:
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://aeroapi.flightaware.com/aeroapi'

    def _build_headers(self):
        return {
            'x-apikey': self.api_key,
        }

    def query(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = self.base_url + endpoint
        headers = self._build_headers()
        response = requests.get(url, headers=headers, params=kwargs)

        if response.status_code == 200:
            return response.json()
        else:
            raise requests.HTTPError(f"Error: {response.status_code}, {response.text}")
        

import base64

class JSON_EncoderDecoder():
    """
    GCP service account keys (for auth) are stored as JSON objects, loaded from a file.
    Thie allows you to avoid storing the key in a file.
    
    Encodes and decodes json objects to and from strings.
    This is useful for storing json objects in environment variables.

    """
    def __init__(self, json_object):
        self.json_object = json_object

    def encode(self):
        '''encodes json to a string which can be stored in 
        an environment variable'''
        assert isinstance(self.json_object, dict), 'Variable to encode must be a dict.'
        x = json.dumps(self.json_object)
        self.json_object = base64.b64encode(x.encode('utf-8'))
        return self
    
    def decode(self):
        '''decodes json from a string which can be stored in 
        an environment variable'''
        assert isinstance(self.json_object, str), 'Variable to decode must be a string.'
        x = str(self.json_object)[2:-1]
        self.json_object = json.loads(base64.b64decode(x).decode('utf-8'))
        return self
    
    def get(self):
        return self.json_object



# gcp.py
import os
from google.oauth2 import service_account
from google.cloud import storage
import json
from dotenv import load_dotenv

class GCPClient:
    def __init__(self):
        self.creds_json = self.get_gcp_creds_json()
        self.storage_client = self.init_storage_client()
        self.creds_encoded = self.get_gcp_creds_encoded()
        
    def get_gcp_creds_json(self):
        load_dotenv()
        gcp_creds_encoded = os.getenv("GCP_CREDENTIALS_JSON_ENCODED")
        gcp_creds_json = JSON_EncoderDecoder(gcp_creds_encoded).decode().get()
        return gcp_creds_json

    def init_storage_client(self):
        gcp_credentials = service_account.Credentials.from_service_account_info(self.creds_json)
        storage_client = storage.Client(credentials=gcp_credentials)
        return storage_client
    
    def get_gcp_creds_encoded(self):
        load_dotenv()
        return os.getenv("GCP_CREDENTIALS_JSON_ENCODED")
