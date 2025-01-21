"""
Test DuckDB plugin.

---
Parent task: PythonInstanceTask
---

## Some tmp notes
"""
import os
from typing_extensions import Annotated

import pyarrow as pa
import pandas as pd
from flytekit import kwtypes, task, workflow
from flytekit.types.structured import StructuredDataset
from flytekitplugins.duckdb import DuckDBQuery


def _gen_df() -> pd.DataFrame:
    return pd.DataFrame({
        "name": ["John", "Sam"],
        "height": [171, 190]
    })


s_all_query = DuckDBQuery(
    name="s-all",
    query="SELECT * from df",
    inputs=kwtypes(df=pd.DataFrame)
)


@workflow
def pd_wf() -> pd.DataFrame:
    df = _gen_df()
    return s_all_query(df=df)


if __name__ == "__main__":
    print(f"Test DuckDBQuery...\n")

    # Set query here ...

    print(">>> QUERY RESULT <<<")
    print(pd_wf())