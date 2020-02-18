"""
This is the DAG that will show you one interesting specific of how Livy works
in local mode vs in YARN mode (job running in cluster mode).
This DAG runs an intentionally failing Livy batch.
TODO doc
"""
from datetime import datetime

from airflow import DAG

try:
    # Import statement for Airflow when it loads new operators into airflow.operators
    from airflow.operators import LivyBatchOperator
except ImportError:
    # Import statement for IDE with the local folder structure
    from airflow_home.plugins.livy_batch_plugin import LivyBatchOperator

dag = DAG(
    "04_batch_example_failing",
    description="Running Spark jobs via Livy Batches, intentionally failing the job",
    schedule_interval=None,
    start_date=datetime(1970, 1, 1),
    catchup=False,
)

t1 = LivyBatchOperator(
    name="batch_example_failing_{{ run_id }}",
    file="file:///data/batches/join_2_files.py",
    py_files=["file:///data/batches/join_2_files.py"],
    arguments=[
        "file:///data/grades.csv",
        "file:///data/ssn-address.tsv",
        "-file1_sep=,",
        "-file1_header=true",
        "-file1_schema=`Last name` STRING, `First name` STRING, SSN STRING, "
        "Test1 INT, Test2 INT, Test3 INT, Test4 INT, Final INT, Grade STRING",
        "-file1_join_column=SSN",
        "-file2_header=false",
        "-file2_schema=`Last name` STRING, `First name` STRING, SSN STRING, "
        "Address1 STRING, Address2 STRING",
        "-file2_join_column=SSN",
        "-output_header=true",
        "-output_columns=file1.Inexistent",
    ],
    conf={"spark.submit.deployMode": "cluster"},
    task_id="livy_batch_example_failing",
    dag=dag,
)