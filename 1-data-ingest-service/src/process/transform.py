import pandas as pd

def rename_columns_remove_periods(dataframe):
    new_columns = dataframe.columns.str.replace(".", "_")
    dataframe = dataframe.rename(columns=dict(zip(dataframe.columns, new_columns)))
    return dataframe

def create_crt_ts_cols(df, current_time):
    df['crt_ts'] = pd.to_datetime(current_time)
    df['crt_ts_year'] = df['crt_ts'].dt.year
    df['crt_ts_month'] = df['crt_ts'].dt.month
    df['crt_ts_day'] = df['crt_ts'].dt.day
    df['crt_ts_hour'] = df['crt_ts'].dt.hour
    return df

def datatype_cleanup(df):
    df['codeshares'] = df['codeshares'].astype(str)
    df['codeshares_iata'] = df['codeshares_iata'].astype(str)
    return df

