# gcp.py
import os
from google.oauth2 import service_account
from google.cloud import storage
import json
from dotenv import load_dotenv
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




class GCPClient:
    """
    Instantiate a GCP client object for accessing GCP services,

    Attributes:
        creds_json (dict): GCP credentials JSON
        storage_client (google.cloud.storage.client.Client): GCP storage client
        creds_encoded (str): GCP credentials JSON encoded as a string
    
    Args:
        None, just loads credentials from .env file

    """
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
