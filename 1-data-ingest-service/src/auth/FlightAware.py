import requests
import base64
import json
from datetime import datetime as dt
from typing import Dict, Any
import os

from dotenv import load_dotenv


class FlightAwareAPI:
    
    def __init__(self):
        self.api_key = os.getenv('FLIGHTAWARE_API_KEY')

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