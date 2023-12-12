import json
import base64
import logging
import functions_framework
import pandas as pd
from src.io.encode import decode_pubsub_message
from src.ingest import ingest

def convert_message_to_dataframe(cloud_event):
    """
    Converts a CloudEvent message to a Pandas DataFrame.
    """
    # parse the CloudEvent message
    pubsub_message = cloud_event.data["message"]["data"]
    logging.debug(f'Encoded Pub/Sub Message: {pubsub_message}')
    
    # decode the Pub/Sub message from base64
    messages_json = decode_pubsub_message(pubsub_message)
    if messages_json is None:
        raise ValueError("Decoding returned None")
    logging.info(f'Decoded Pub/Sub Message: {messages_json}')
    
    # convert the JSON Pub/Sub message to a dataframe
    df = pd.json_normalize(messages_json['data'], meta=messages_json['schema'])
    logging.debug(f"DataFrame: \n{df}\nTypes: \n{df.dtypes}")
    return df


@functions_framework.cloud_event
def main(cloud_event):
    """
    Processes a CloudEvent from a Cloud Pub/Sub topic.
    """
    try:
        df = convert_message_to_dataframe(cloud_event)

    except Exception as e:
        logging.error(f"Error in cloud event conversion to dataframe: {e}")

    try:
        ingest(df=df) # ingest the data based on input dataframe contents

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        raise e