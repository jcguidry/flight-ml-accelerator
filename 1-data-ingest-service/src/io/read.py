import pandas as pd
import requests
import logging


def get_flight_data(api, identifier, start_datetime, end_datetime, max_pages=40):
    """
    Get flight data from FlightAware API, given an identifier and a time range.
    """
    endpoint_base = '/flights/'
    endpoint = f'{endpoint_base}{identifier}'
    try:
        data = api.query(endpoint, 
                end= end_datetime, 
                start= start_datetime, 
                max_pages=max_pages)

    except requests.HTTPError as e:
        print(e)
    except Exception as e:
        logging.error(f"An unexpected Flight API error occurred: {e}")

    df = pd.json_normalize(data, 'flights')

    return df


def get_airport_departures(api, airport_id, start_datetime, end_datetime, max_pages='5', cursor='1'):
    """
    # Get 
    """
    
    endpoint = f'/airports/{airport_id}/flights/departures'
    airline = 'AAL'
    try:
        data = api.query(endpoint, 
                airline = airline,
                end= end_datetime, 
                start= start_datetime, 
                max_pages=max_pages,
                cursor=cursor)

    except requests.HTTPError as e:
        print(e)
    except Exception as e:
        logging.error(f"An unexpected Flight API error occurred: {e}")

    return pd.json_normalize(data, 'departures')


