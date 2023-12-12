import functions_framework
import json
import base64
import logging
import pandas as pd
from src.ingest import ingest
from src.io.encode import encode_pubsub_message

from main import main


class MockCloudEvent:
    """
    Mock CloudEvent for testing to match format from PubSub.
    """
    def __init__(self, data):
        self.data = data


def create_test_data():
    
    # begin with a list of flight identifiers, as dictionary
    flight_ident_list = [{'flight_ident': 'AA2563', 'ingest_type': 'latest'},
                        {'flight_ident': 'AA2227', 'ingest_type': 'latest'},]
    
    #convert to dataframe, with schema
    df = pd.DataFrame(flight_ident_list)#.convert_dtypes(dtype_backend='pyarrow')
    
    #convert to json, then encode to base64
    df_json = df.to_json(orient='table')
    df_json_encoded = encode_pubsub_message(df_json)
    
    payload = {'message': {'data': df_json_encoded}}

    # create object with data attribute, like a CloudEvent
    mock_cloud_event = MockCloudEvent(payload)

    return mock_cloud_event


def test_main():
    
    mock_cloud_event = create_test_data()

    main(mock_cloud_event)
    

if __name__ == "__main__":
    test_main()