from google.cloud import bigquery
from fastapi import Depends
from typing import Annotated

def get_bigquery_client():
    client = bigquery.Client()
    return client

BigQueryClientDependency = Annotated[bigquery.Client, Depends(get_bigquery_client)]
