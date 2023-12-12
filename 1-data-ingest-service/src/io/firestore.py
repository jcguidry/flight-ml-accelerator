import pandas as pd
from google.cloud import firestore
 

def get_last_run_timestamp(identifier, firestore_client):
    doc_ref = firestore_client.collection('flight_timestamps').document(identifier)
    doc = doc_ref.get()
    if doc.exists:
        return pd.Timestamp(doc.get('last_run_ts'))
    else:
        print('No existing timestamp, returning early timestamp.')
        return pd.Timestamp('2000-01-01 00:00:00')

def update_last_run_timestamp(identifier, timestamp, firestore_client):
    doc_ref = firestore_client.collection('flight_timestamps').document(identifier)
    doc_ref.set({'last_run_ts': timestamp})

###### For scheduled out columns

def update_scheduled_out(fa_flight_ids, scheduled_outs, firestore_client):
    for flight_id, scheduled_out in zip(fa_flight_ids, scheduled_outs):
        doc_ref = firestore_client.collection('flight_scheduled_out').document(str(flight_id))
        doc_ref.set({'scheduled_out': scheduled_out})


def get_scheduled_out_prev_ts(fa_flight_ids, firestore_client):
    scheduled_out_dict = {}
    for flight_id in fa_flight_ids:
        doc_ref = firestore_client.collection('flight_scheduled_out').document(str(flight_id))
        doc = doc_ref.get()
        if doc.exists:
            scheduled_out_dict[flight_id] = pd.Timestamp(doc.get('scheduled_out'))
        else:
            scheduled_out_dict[flight_id] = None
    return scheduled_out_dict


