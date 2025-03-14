from airflow import DAG 
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json 



##Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    ##step 1: Create the table if it does not exist
    @task 
    def create_table():
        # initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")

        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        explanation TEXT,
        url TEXT,
        date DATE,
        media_type VARCHAR(50)
        );
        
        """
        ## Execute the table creation query
        postgres_hook.run(create_table_query)


    ##step 2: Extrach the NASA APT(APOD)-Astronomy Picture of the Day[Extract pipeline]
    extract_apod=SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api', ## Connection ID Defined In Airflow For NASA API
        endpoint='planetary/apod', ## NASA API endpoint for APOD
        method='GET',   
        data={"api_key":"{{ conn.nasa_api.extra_dejson.api_key}}"},## use the API key from the connection
        response_filter=lambda response:response.json(),## convert response to json
    )

    ##step 3:Transform the data(Pick the information that i need to save)
    @task
    def transform_apod_data(response):
        apod_data={
            'title':response.get('title',''),
            'explanation':response.get('explanation',''),
            'url':response.get('url',''),
            'date':response.get('date',''),
            'media_type':response.get('media_type','')
        }
        return apod_data

    ##step 4: Load the data into the database(postgres sql)
    @task
    def load_data_into_postgres(apod_data):
        # initialize the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")

        ## Define the SQl insert Query
        insert_query=""" 
        INSERT INTO apod_data (title,explanation,url,date,media_type)
        VALUES (%s,%s,%s,%s,%s);
        """
        ## Execute the insert query
        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))


    ##step 5:verify the data with DBViewer 


    ##step 6: Define the task dependecies 
    #EXTRACT
    create_table() >> extract_apod ## ensure the table is created before extraction 
    api_response=extract_apod.output
    
    #TRANSFORM
    transformed_data=transform_apod_data(api_response)
    
    #LOAD 
    load_data_into_postgres(transformed_data) ## ensure the data is loaded into the database after 