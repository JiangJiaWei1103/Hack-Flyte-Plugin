"""
Test Snowflake agent.

---
Executor: AsyncAgentExecutorMixin
Parent task: SQLTask 
---

## Some tmp notes
* [ ] What's a snowflake handler
* [ ] Every get_<x> method in Task can be accessed through task_template.x?
    * e.g., get_config, get_sql in this agent and get_custom in others?
* [ ] Switch to key pair authentication 
    * Use password now
* [ ] Python string interpolation

* Curcular import if naming this file as snowflake.py
    * https://stackoverflow.com/questions/72717979/python-importerror-cannot-import-name-from-partially-initialized-module
"""
import pandas as pd
from flytekit import Secret, StructuredDataset, kwtypes, task, workflow
from flytekitplugins.snowflake import SnowflakeConfig, SnowflakeTask


"""
You can get the SnowflakeConfig's metadata from the Snowflake console by executing the following query:

SELECT
    CURRENT_USER() AS "User",
    CONCAT(CURRENT_ORGANIZATION_NAME(), '-', CURRENT_ACCOUNT_NAME()) AS "Account",
    CURRENT_DATABASE() AS "Database",
    CURRENT_SCHEMA() AS "Schema",
    CURRENT_WAREHOUSE() AS "Warehouse";
"""


snowflake_task_insert_query = SnowflakeTask(
    name="insert-query",
    inputs=kwtypes(c1=int, c2=str),
    task_config=SnowflakeConfig(
        user="ABAOJIANG",
        account="FBXRGAF-HMB83142",
        warehouse="tiny_flyte",
        database="tiny_flyte_db",
        schema="tiny_flyte_schema",
    ),
    query_template="""
    INSERT INTO tiny_flyte_db.tiny_flyte_schema.tiny_flyte_table (c1, c2)
    VALUES (%(c1)s, %(c2)s);
    """,
)


snowflake_task_templatized_query = SnowflakeTask(
    name="select-query",
    output_schema_type=StructuredDataset,
    task_config=SnowflakeConfig(
        user="ABAOJIANG",
        account="FBXRGAF-HMB83142",
        warehouse="tiny_flyte",
        database="tiny_flyte_db",
        schema="tiny_flyte_schema",
    ),
    query_template="SELECT * FROM tiny_flyte_db.tiny_flyte_schema.tiny_flyte_table;"
)


@task(
    secret_requests=[
        Secret(
            group="private-key",
            key="snowflake",
        )
    ],
)
def print_head(input_sd: StructuredDataset) -> pd.DataFrame:
    df = input_sd.open(pd.DataFrame).all()
    print(df)
    return df


@workflow
def wf() ->  None:
    sd = snowflake_task_templatized_query()
    t1 = print_head(input_sd=sd)
    insert_query = snowflake_task_insert_query(c1=2000, c2="2thousand")
    sd2 = snowflake_task_templatized_query()
    t2 = print_head(input_sd=sd2)

    # Chain queries 
    sd >> t1 >> insert_query >> sd2 >> t2


if __name__ == "__main__":
    wf()