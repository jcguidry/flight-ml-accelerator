#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys

# if notebook is being run from src directory, change to root directory
if os.getcwd().split(os.sep)[-1] == 'src':
    try:
        sys.path.remove('')
        sys.path.append('../')
    except: pass


# In[2]:


# Base Libraries
import os
import json
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime as dt
from datetime import timedelta 
import pandas as pd

from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import firestore

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
logging.basicConfig(level=logging.INFO)


# In[3]:


from src.auth.gcp import GCPClient
from src.auth.FlightAware import FlightAwareAPI

from src.io.read import get_flight_data
from src.io.firestore import get_last_run_timestamp, update_last_run_timestamp, get_scheduled_out_prev_ts, update_scheduled_out
from src.process.transform import rename_columns_remove_periods, create_crt_ts_cols, datatype_cleanup
from src.io.write import write_to_gcs


# In[4]:


def ingest(df):
    """
    Given a dataframe of flight identifiers and ingestion options, 
    query the FlightAware API for flight data and write to GCS.
    """

    identifier = df.iloc[0]['flight_ident']


    # ------ PARAMETERS ------ 
    lookback_hours = 7*24 # how many hours back to query, based on the flight's actual departure
    lookfoward_hours = 2*24 # how many hours forward to query, based on the flight's scheduled departure
    bucket_name = 'datalake-flight-dev-1'
    blob_name = 'flightsummary-ingest-raw-json'
    project_id = 'aia-ds-accelerator-flight-1'


    # ------ INITIALIZE SERVICE CLIENTS ------
    gcp_client = GCPClient()
    gcp_credentials = gcp_client.credentials    
    firestore_client = firestore.Client(credentials=gcp_credentials, project=project_id)
    storage_client = storage.Client(credentials=gcp_credentials, project=project_id)
    # pubsub_client = pubsub_v1.PublisherClient(credentials= gcp_credentials)
    FA_client = FlightAwareAPI()

    # ------ DERIVED TIMESTAMPS ------      
    current_time_raw = dt.utcnow()

    current_time = current_time_raw.strftime('%Y-%m-%dT%H:%M:%SZ')
    query_start = (current_time_raw - timedelta(hours=lookback_hours)).strftime('%Y-%m-%dT%H:%M:%SZ')
    query_end = (current_time_raw + timedelta(hours=lookfoward_hours)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # ------ READ ------
    df = get_flight_data(FA_client, identifier, query_start, query_end)

    # --- PROCESS ---
    # Rename columns with '.' in the name.
    df = rename_columns_remove_periods(df)
    # Convert certain columns to string to avoid errors
    df = datatype_cleanup(df)
    # Add current run timestamp to the dataframe
    df = create_crt_ts_cols(df, current_time = current_time)


    # ------ STATE MANAGEMENT ------
    # --- Obtain the last run timestamp(s) for the flight_id(s) in the query.
    last_run_ts = get_last_run_timestamp(identifier, firestore_client)
    df['last_run_ts'] = last_run_ts
    print(f'last query run timestamp: {last_run_ts}')

    # --- Obtain latest 'scheduled out' timestamp for each flight ID
    scheduled_out_dict = df.groupby('fa_flight_id')['scheduled_out'].first().to_dict()
    scheduled_out_prev_dict = get_scheduled_out_prev_ts(df['fa_flight_id'].unique(), firestore_client)
    df['last_scheduled_out_ts'] = df['fa_flight_id'].map(scheduled_out_prev_dict)


        # ------ WRITE ------
    try:
        write_to_gcs(df, bucket_name, blob_name, storage_client)
    except Exception as e:
        logging.error(f"error when writing data: {e}")


    # Update the query last run timestamp in Firestore
    update_last_run_timestamp(identifier, current_time, firestore_client)

    # Update Firestore with the current 'scheduled_out' values
    update_scheduled_out(scheduled_out_dict.keys(), scheduled_out_dict.values(), firestore_client)


# In[5]:


# Prevents main() from being called when the module is imported

if __name__ == "__main__":
    pass


# In[6]:


# TESTING

# # begin with a list of flight identifiers, as dictionary
# flight_ident_list = [{'flight_ident': 'AA2563', 'ingest_type': 'latest'},
#                     {'flight_ident': 'AA2227', 'ingest_type': 'latest'},]

# #convert to dataframe, with schema
# df = pd.DataFrame(flight_ident_list)#.convert_dtypes(dtype_backend='pyarrow')

# ingest(df)

