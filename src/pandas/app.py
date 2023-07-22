import pandas as pd
import s3fs
from io import BytesIO


def lambda_handler(event, context):
    s3 = s3fs.S3FileSystem(key='', 
                           secret='')
    bucket = 'confessions-of-a-data-guy'  
    prefix = 'harddrives'
    
    all_data = pd.DataFrame()
    
    files = s3.ls(f's3://{bucket}/{prefix}/')
    for file in files:
        if '.csv' not in file:
            continue
        print(f"Reading {file}")
        with s3.open(file, 'rb') as f:
            df = pd.read_csv(BytesIO(f.read()), engine='pyarrow')
            all_data = pd.concat([all_data, df], ignore_index=True)


    failures_per_day = all_data.groupby(['date'])['failure'].sum().reset_index()


    with s3.open(f's3://{bucket}/results/failures.csv', 'wb') as f:
        failures_per_day.to_csv(f)

