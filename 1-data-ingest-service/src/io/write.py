
from datetime import datetime as dt
import logging

def write_to_gcs(df, bucket_name, blob_name, client):
    # client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    for year, year_df in df.groupby('crt_ts_year'):
        for month, month_df in year_df.groupby('crt_ts_month'):
            for day, day_df in month_df.groupby('crt_ts_day'):
                for flight_id, flight_df in day_df.groupby('ident'):
                    timestamp_str = dt.strftime(flight_df['crt_ts'].max(), '%Y%m%d%H%M%S')
                    blob_name = f'{blob_name}/year={year}/month={month}/day={day}/{flight_id}/{timestamp_str}.json'
                    blob = bucket.blob(blob_name)
                    blob.upload_from_string(flight_df.to_json(orient='records'))



# topic_name = "flight-summary-ingest-raw"
def write_to_pubsub(df, topic_name, pubsub_client, project_id):
    try:
        json_data = df.to_json(orient='records', lines=True)    
        topic_path = pubsub_client.topic_path(project_id, topic_name)
        for record in json_data.splitlines():
            pubsub_client.publish(topic_path, data=record.encode('utf-8'))    
    except Exception as e:
        logging.error(f"error when publishing to pubsub: {e}")