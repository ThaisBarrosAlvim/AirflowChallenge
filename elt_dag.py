import os
import sqlite3
import pandas as pd
from airflow.utils.edgemodifier import Label
from datetime import datetime, timedelta
from textwrap import dedent
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.models import Variable

DB_PATH = os.path.join('data', 'Northwind_small.sqlite')
OUTPUT_FILE = 'output_orders.csv'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


## Do not change the code below this line ---------------------!!#
def export_final_answer():
    import base64

    # Import count
    with open('count.txt') as f:
        count = f.readlines()[0]

    my_email = Variable.get("my_email")
    message = my_email+count
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    with open("final_output.txt","w") as f:
        f.write(base64_message)
    return None
## Do not change the code above this line-----------------------##

def extract_orders_to_csv(**kwargs):
    """ Function to extract data from the "Order" table and generate a CSV file """
    conn = sqlite3.connect(DB_PATH)

    query = "SELECT * FROM 'Order'"
    df = pd.read_sql_query(query, conn)

    # Save the DataFrame to a CSV file
    df.to_csv(OUTPUT_FILE, index=False)

    conn.close()


def calculate_rio_quantity_sum(**kwargs):
    """
    Reads the "OrderDetail" table from the database, performs a JOIN with "output_orders.csv,"
    calculates the sum of Quantity for orders where ShipCity = 'Rio de Janeiro,'
    and writes the result to "count.txt."
    """
    orders_df = pd.read_csv(OUTPUT_FILE)

    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM 'OrderDetail'"
    order_detail_df = pd.read_sql_query(query, conn)
    conn.close()

    #  JOIN between "OrderDetail.OrderId" and "Order.Id"
    merged_df = pd.merge(
        order_detail_df,
        orders_df,
        left_on='OrderId',
        right_on='Id',
        how='inner'
    )

    # Filter rows where ShipCity = 'Rio de Janeiro'
    filtered_df = merged_df[merged_df['ShipCity'] == 'Rio de Janeiro']

    total_quantity = filtered_df['Quantity'].sum()

    with open('count.txt', 'w') as f:
        f.write(str(total_quantity))

with DAG(
    'DesafioAirflow',
    default_args=default_args,
    description='Desafio de Airflow da Indicium',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = """
        Esse é o desafio de Airflow da Indicium.
    """
    
     # Task to extract data from "Order" and save it as a CSV
    extract_orders_task = PythonOperator(
        task_id='extract_orders',
        python_callable=extract_orders_to_csv,
        provide_context=True
    )

    # Task to calculate the total Quantity for orders to "Rio de Janeiro" and save to count.txt
    calculate_rio_quantity_task = PythonOperator(
        task_id='calculate_rio_quantity',
        python_callable=calculate_rio_quantity_sum,
        provide_context=True
    )

    # Task to generate the final output encoded in base64
    export_final_output = PythonOperator(
        task_id='export_final_output',
        python_callable=export_final_answer,
        provide_context=True
    )

    extract_orders_task >> calculate_rio_quantity_task >> export_final_output
