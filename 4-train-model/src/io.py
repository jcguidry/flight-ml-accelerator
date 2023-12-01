
try:
    from gcp import GCPClient  # Relative import
except ImportError:
    from src.gcp import GCPClient  # Absolute import as fallback

from gcsfs import GCSFileSystem

import pandas as pd
import polars as pl
from deltalake import DeltaTable
from deltalake.writer import write_deltalake

import pyarrow
from datetime import date, datetime, timedelta
import json


class DataLoader:
    # instantiate object for generically loading data from a GCS bucket

    def __init__(self, client):
        self.client = client
        self.dataset = None

        # config for reading with pyarrow
        self.storage_options = {"service_account_key": json.dumps(client.creds_json)}
        fs = pyarrow.fs.GcsFileSystem(access_token=client.creds_encoded, 
                                      credential_token_expiration = datetime.fromisoformat('9999-12-31') )


    def get_date_from_lookback(self, lookback_days: int, return_as_str = True):
        '''Returns a date object or string for a given number of days in the past
           Often we want to query a table for the last N days.'''
        
        target_date = datetime.utcnow() - timedelta(days=lookback_days)
        
        if return_as_str:
            year, month, day = target_date.year, target_date.month, target_date.day
            return f'{year}/{month:02d}/{day:02d}'
        else:
            return target_date


    def load_delta_table(self, path, lookback_params= None):
        '''Loads a delta table from a GCS bucket, as a pyarrow dataset. 
            This can then be converted to a pandas dataframe or polars dataframe.
              
            Optionally, you can pass in a dictionary of parameters to filter the table by date.
            
            example parameters for filtering
                lookback_params = {
                        'lookback_days': 1000,
                        'lookback_date_column': 'crt_ts_date'}
            
            This is useful for loading a table for training, where we only want to load the last N days.
            Should also add additional parameters for generic partition column filtering.
        '''

        dt = DeltaTable(table_uri=path, 
                        storage_options=self.storage_options,
                        without_files=False)

        if lookback_params is not None:


            query_date = self.get_date_from_lookback(lookback_days = lookback_params['lookback_days'])
            date_column = lookback_params['lookback_date_column']
            self.dataset = dt.to_pyarrow_dataset(partitions=[(date_column, ">=", query_date)])
        else:
            self.dataset = dt.to_pyarrow_dataset()



    def return_as_pandas(self):
        '''Returns the loaded pyarrow dataset as a pandas dataframe'''
        if self.dataset is None:
            raise ValueError('Must have delta table loaded first')        
        return self.dataset.to_table().to_pandas(types_mapper=pd.ArrowDtype)

    def return_as_polars_df(self):
        ''' Returns the loaded pyarrow dataset as a polars dataframe'''
        if self.dataset is None:
            raise ValueError('Must have delta table loaded first')
        # return pl.from_arrow(self.dataset.to_table())
        return pl.scan_pyarrow_dataset(self.dataset).collect()

    
    def return_as_polars_df_lazy(self):
        ''' Returns the loaded pyarrow dataset as a polars lazyframe'''
        if self.dataset is None:
            raise ValueError('Must have delta table loaded first')
        return pl.scan_pyarrow_dataset(self.dataset)


class DataWriter:
    ''''
    Writes data to GCS bucket, in delta table format by default. 
    Detects if the data is a pandas or polars dataframe, and writes accordingly.
    Optionally, can write to a local parquet file.
    '''

    def __init__(self, df):
        self.df = df

        self.write_methods = {
            'pandas': {
                'parquet': lambda path, **kwargs: self.df.to_parquet(path, **kwargs),
                'csv': lambda path, **kwargs: self.df.to_csv(path, **kwargs),
                'delta': lambda path, **kwargs: write_deltalake(path, pyarrow.Table.from_pandas(self.df), mode='overwrite', overwrite_schema=True ) 
            },
            'polars': {
                'parquet': lambda path, **kwargs: self.df.write_parquet(path),
                'csv': lambda path, **kwargs: self.df.write_csv(path, **kwargs),
                'delta': lambda path, **kwargs: self.df.write_delta(path, mode='overwrite', overwrite_schema=True, **kwargs )
            },
            'polars_lazy': {
                'parquet': lambda path, **kwargs: self.df.collect().write_parquet(path),
                'csv': lambda path, **kwargs: self.df.collect().write_csv(path, **kwargs),
                'delta': lambda path, **kwargs: self.df.collect().write_delta(path, mode='overwrite', overwrite_schema=True, **kwargs)
            }
        }

        if isinstance(self.df, pd.core.frame.DataFrame):
            self.df_type = 'pandas'
        elif isinstance(self.df, pl.dataframe.frame.DataFrame):
            self.df_type = 'polars'
        elif isinstance(self.df, pl.lazyframe.frame.LazyFrame):
            self.df_type = 'polars_lazy'
        else:
            raise ValueError('Dataframe must be either a pandas or polars dataframe')


    def detect_file_suffix(self):
        if self.file_type_out == 'parquet':
            return '.parquet'
        elif self.file_type_out == 'csv':
            return '.csv'
        elif self.file_type_out == 'delta':
            return ''
        else:
            raise ValueError('File type must be either parquet, csv, or delta')

    def select_write_method(self):
        return self.write_methods[self.df_type][self.file_type_out]
    

    def write_local(self, path: str, file_type_out: str = 'parquet'):
        self.file_type_out = file_type_out
        write_method = self.select_write_method()
        file_suffix = self.detect_file_suffix()

        path_full = path+file_suffix
        write_method(path_full)
        print(f"Writing data to {path_full}")


    def write_gcs(self, path: str, client, file_type_out: str = 'parquet'):
        self.file_type_out = file_type_out
        
        write_method = self.select_write_method()
        file_suffix = self.detect_file_suffix()
        path_full = path+file_suffix

        storage_options = {"service_account_key": json.dumps(client.creds_json)}
        fs = pyarrow.fs.GcsFileSystem(access_token=client.creds_encoded, 
                                      credential_token_expiration = datetime.fromisoformat('9999-12-31') )

        write_method(path_full, storage_options = storage_options)
        print(f"Writing data to {path_full}")



## Example usage

# gcs_path_prefix = 'gs://datalake-flight-dev-1/'
# table_path_in = f'{gcs_path_prefix}flightsummary-delta-processed-stream/'

# table_name_out = 'flightsummary-delta-processed-training'
# table_path_out = f'{gcs_path_prefix}training/{table_name_out}'
# table_path_out_local = f'../data/{table_name_out}'

# client = GCPClient()
# dl = DataLoader(client=client)

# lookback_params = {
#     'lookback_days': 1000,
#     'lookback_date_column': 'crt_ts_date'}


# dl.load_delta_table(path=table_path_in, lookback_params=lookback_params)

# # df = dl.return_as_pandas()
# df = dl.return_as_polars_df()
# df.schema
# # dl.return_as_polars_df_lazy()


# dw = DataWriter(df)

# dw.write_local(path=table_path_out_local, file_type_out='parquet')
# dw.write_local(path=table_path_out_local, file_type_out='csv')
# dw.write_local(path=table_path_out_local, file_type_out='delta')


# dw.write_gcs(path=table_path_out, client=client, file_type_out='parquet')
# dw.write_gcs(path=table_path_out, client=client, file_type_out='csv')
# dw.write_gcs(path=table_path_out, client=client, file_type_out='delta')