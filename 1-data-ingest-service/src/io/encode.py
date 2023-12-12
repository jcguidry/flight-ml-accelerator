import json
import base64
import logging

def encode_pubsub_message(message_json):
    """
    Encodes a JSON object into a base64 string.
    """
    try:
        json_str = json.dumps(message_json)
        return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    except Exception as e:
        logging.error(f"Error in encoding: {e}")
        return None
    
def decode_pubsub_message(pubsub_message):
    """
    Decodes a Pub/Sub message from base64 encoding to a list of JSON objects.
    """
    try:
        decoded_str = base64.b64decode(pubsub_message).decode('utf-8')
        return json.loads(decoded_str)
    except Exception as e:
        logging.error(f"Error in decoding: {e}")
        return None