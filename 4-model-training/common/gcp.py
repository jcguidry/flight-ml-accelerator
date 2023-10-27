# gcp.py
import os
from google.oauth2 import service_account
from google.cloud import storage
from utils import JSON_EncoderDecoder
import json
from dotenv import load_dotenv


class GCPClient:
    def __init__(self):
        self.creds_json = self.get_gcp_creds_json()
        self.storage_client = self.init_storage_client()
        
    def get_gcp_creds_json(self):
        load_dotenv()
        gcp_creds_encoded = os.getenv("GCP_CREDENTIALS_JSON_ENCODED")
        gcp_creds_json = JSON_EncoderDecoder(gcp_creds_encoded).decode().get()
        return gcp_creds_json

    def init_storage_client(self):
        gcp_credentials = service_account.Credentials.from_service_account_info(self.creds_json)
        storage_client = storage.Client(credentials=gcp_credentials)
        return storage_client