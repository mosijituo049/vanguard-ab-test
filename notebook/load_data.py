import pandas as pd
import yaml
from google.cloud import bigquery

with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

def query_funnel():
    try:
        client = bigquery.Client()
        query_funnel = f"""
        SELECT *
        FROM {config['tables']['mart_funnel']}
        """
        df_funnel = client.query(query_funnel).to_dataframe()
        df_funnel.to_csv(config['path']['funnel'],index=False)
        print("funnel table loaded!")
        return df_funnel
    except Exception as e:
        print(e)
        return pd.DataFrame() 

def query_duration():
    try:
        client = bigquery.Client()
        query_duration = f"""
        SELECT *
        FROM {config['tables']['mart_duration']}
        """
        df_duration = client.query(query_duration).to_dataframe()
        df_duration.to_csv(config['path']['duration'],index=False)
        print("duration table loaded!")
        return df_duration
    except Exception as e:
        print(e)
        return pd.DataFrame()   

def query_transition():
    try:
        client = bigquery.Client()
        query_transition = f"""
        SELECT *
        FROM {config['tables']['mart_transition']}
        """
        df_transition = client.query(query_transition).to_dataframe()
        df_transition.to_csv(config['path']['transition'],index=False)
        print("transition table loaded!")
        return df_transition
    except Exception as e:
        print(e)
        return pd.DataFrame()    

def query_completion_time():
    try:
        client = bigquery.Client()
        query_completion_time = f"""
        SELECT *
        FROM {config['tables']['mart_completion_time']}
        """
        df_completion_time = client.query(query_completion_time).to_dataframe()
        df_completion_time.to_csv(config['path']['completion_time'],index=False)
        print("completion time table loaded!")
        return df_completion_time
    except Exception as e:
        print(e)
        return pd.DataFrame()

def query_client():
    try:
        client = bigquery.Client()
        query_client = f"""
        SELECT *
        FROM {config['tables']['int_client_dimension']}
        """
        df_client = client.query(query_client).to_dataframe()
        df_client.to_csv(config['path']['client'],index=False)
        print("client table loaded!")
        return df_client
    except Exception as e:
        print(e)
        return pd.DataFrame()               

def query(table):
    if table == "funnel":
        return query_funnel()
    
    elif table == "duration":
        return query_duration()
    
    elif table == "transition":
        return query_transition()
    
    elif table == "completion_time":
        return query_completion_time()
    
    elif table == "client":
        return query_client()
    
    else:
        print(f"{table} doesn't exist!")
        return pd.DataFrame() 

def load(table):
    try:
        df = pd.read_csv(f"../data/clean/{table}.csv")
    except FileNotFoundError:
        print("csv doesn't exist, loading from database...")
        return query(table)
    except pd.errors.EmptyDataError:
        print("csv is empty, reloading data from database...")
        return query(table)
    except Exception as e:
        print("failed to read csv, reloading data from database...")
        return query(table)
    else:
        print(f"{table} table loaded!")
        return df

def reload():
    query_funnel()
    query_duration()
    query_transition()
    query_completion_time()
    query_client()
    print("all tables reloaded!")


if __name__ == "__main__":
    table = input("what table you want to load?")
    df = load(table)
    df.head()
