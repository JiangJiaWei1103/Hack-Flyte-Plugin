"""
Test BigQuery agent.
"""
from typing_extensions import Annotated

import pandas as pd
from flytekit import kwtypes
from flytekit.types.structured import StructuredDataset
from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask


# Define bq task
DogeCoinDataset = Annotated[StructuredDataset, kwtypes(hash=str, size=int, block_number=int)]
bq_doge_coin = BigQueryTask(
    name=f"bigquery.doge_coin",
    inputs=kwtypes(version=int),
    query_template="SELECT * FROM `bigquery-public-data.crypto_dogecoin.transactions` WHERE version = @version LIMIT 10;",
    output_structured_dataset_type=DogeCoinDataset,
    task_config=BigQueryConfig(ProjectID="test-bq-agent")
)


# Define another task
# ...


# Define wf
# ...



if __name__ == "__main__":
    df = bq_doge_coin(version=10).open(pd.DataFrame).all()
    assert isinstance(df, pd.DataFrame)
    
    # Figure out why returned df is empty...
    assert len(df) == 0
    