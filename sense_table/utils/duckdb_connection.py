
import boto3
import duckdb

def get_duckdb_connection():
    return duckdb.connect()

def get_duckdb_connection_s3(s3_client):
    credentials = s3_client._request_signer._credentials
    region = s3_client.meta.region_name
    aws_key = credentials.access_key
    aws_secret = credentials.secret_key
    aws_token = credentials.token  # May be None if not temporary credentials
    con = duckdb.connect()
    # Configure DuckDB S3 settings
    con.execute(f"SET s3_region='{region}'")
    con.execute(f"SET s3_access_key_id='{aws_key}'")
    con.execute(f"SET s3_secret_access_key='{aws_secret}'")
    con.execute('SET parquet_metadata_cache=true')

    if aws_token:
        con.execute(f"SET s3_session_token='{aws_token}'")
    return con


if __name__ == '__main__':
    s3_client = boto3.client('s3')
    from timeit import default_timer

    time_start = default_timer()

    con = get_duckdb_connection(s3_client)
    print(default_timer() - time_start)
    con.execute("SELECT count(*) FROM 's3://sense-table-demo/datasets/COCO2017/bbox.parquet'")
    print(con.fetchall())
    