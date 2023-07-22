import polars as pl
import pyarrow.dataset as ds
import s3fs
import os


os.environ['AWS_ACCESS_KEY_ID']=''
os.environ['AWS_SECRET_ACCESS_KEY']=''


def lambda_handler(event, context):

    bucket = 'confessions-of-a-data-guy'  
    path = 'harddrives'
    fs = s3fs.S3FileSystem(key=os.environ['AWS_ACCESS_KEY_ID'],
                           secret=os.environ['AWS_SECRET_ACCESS_KEY'],
                           config_kwargs={'region_name':'us-east-1'}
                                          )

    s3_endpoint = f"s3://{bucket}/{path}"

    myds = ds.dataset([y for y in fs.ls(s3_endpoint) if ".csv" in y], 
                      filesystem=fs, 
                      format="csv")
    lazy_df = pl.scan_ds(myds)
    sql = pl.SQLContext()
    sql.register("harddrives", lazy_df)   
    results = sql.query("""
                      SELECT date, SUM(failure) as failures
                      FROM harddrives 
                      GROUP BY date
                      """)
    
    with fs.open("s3://confessions-of-a-data-guy/harddrives/results/failures.csv", "w") as f:
        results.write_csv(f)


if __name__ == "__main__":
    lambda_handler(None, None) 
