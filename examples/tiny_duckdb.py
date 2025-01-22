"""
Test DuckDB plugin.

---
Parent task: PythonInstanceTask
---

## Some tmp notes
* Not an agent
    * No extra executor is used, just overriding execute method
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
        "height": [171, 190],
        "salary": [100, 90],
    })


s_all_query = DuckDBQuery(
    name="s-all",
    query="SELECT * FROM df",
    inputs=kwtypes(df=pd.DataFrame)
)


flex_query = DuckDBQuery(
    name="flex",
    inputs=kwtypes(df=pd.DataFrame, query=str)
)


@workflow
def pd_wf(query: str) -> pd.DataFrame:
    df = _gen_df()
    res = s_all_query(df=df)
    res = flex_query(df=res, query=query)

    return res


if __name__ == "__main__":
    print(f"Test DuckDBQuery...\n")

    s_sum = "SELECT SUM(salary) FROM df"

    print(">>> QUERY RESULT <<<")
    print(pd_wf(query=s_sum))