
import boto3
import duckdb
import os
import logging
from typing import Callable
from duckdb import DuckDBPyConnection
from pydantic import validate_call, ConfigDict
from botocore.client import BaseClient


logger = logging.getLogger(__name__)


DuckdbConnectionMaker = Callable[[], DuckDBPyConnection]

@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def duckdb_connection_using_s3(
        s3_client: BaseClient = boto3.client('s3'),
        memory_limit: str = '3GB',
    ) -> DuckdbConnectionMaker:
    def maker():
        con = duckdb.connect()
        credentials = s3_client._request_signer._credentials
        region = s3_client.meta.region_name
        aws_key = credentials.access_key
        aws_secret = credentials.secret_key
        aws_token = credentials.token  # May be None if not temporary credentials
        con = duckdb.connect()
        home_directory = os.getenv('HOME', '/tmp')
        # Set home_directory before httpfs auto-installs
        con.execute(f"SET home_directory='{home_directory}'")
        con.execute(f"SET memory_limit='{memory_limit}'")

        # Now install and load the extension
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")
        # Configure DuckDB S3 settings
        con.execute(f"SET s3_region='{region}'")
        con.execute(f"SET s3_access_key_id='{aws_key}'")
        con.execute(f"SET s3_secret_access_key='{aws_secret}'")
        
        con.execute('SET parquet_metadata_cache=true')

        if aws_token:
            con.execute(f"SET s3_session_token='{aws_token}'")
        return con
    return maker

@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def duckdb_connection_using_one_zone_s3(
        s3_client: BaseClient = boto3.client('s3'),
        zone: str = 'usw2-az1',
) -> DuckdbConnectionMaker:
    def maker():
        con = duckdb_connection_using_s3(s3_client)()
        region = s3_client.meta.region_name
        s3_endpoint = f's3express-{zone}.{region}.amazonaws.com'
        con.execute(f"SET s3_endpoint='{s3_endpoint}'")
        return con
    return maker



def check_permissions(query: str) -> None:
    tokens = [w.lower() for w in query.split() if w]
    forbidden = ['copy', 'export', 'delete', 'attach']
    if any(w in tokens for w in forbidden):
        logger.warning(f"Forbidden query: {query}")
        raise PermissionError("You are only allowed to run readonly queries")


if __name__ == '__main__':
    cm = duckdb_connection_using_one_zone_s3()
    con = cm()
    con.execute("SELECT 1")
    print(con.fetchall())