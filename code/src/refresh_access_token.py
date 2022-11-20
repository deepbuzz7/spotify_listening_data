from dotenv import load_dotenv
import os
import base64
import requests
import psycopg2
import sys
sys.path.insert(1,"/opt/airflow/code")
from src.sql.sql_queries import check_whether_table_is_present_or_not,create_secrets_table

load_dotenv()

def get_connection():
    
    try:
        
        conn = psycopg2.connect(
            host=os.environ.get('host'),
            database=os.environ.get('database_name'),
            user=os.environ.get('user'),
            password=os.environ.get('password')
        )

        cur=conn.cursor()
        return conn,cur
    except (Exception) as error:
        print(error)
    


def get_base64_value(s):
    b64_bytes_encoded=base64.b64encode(s.encode())
    b64_string=b64_bytes_encoded.decode()
    return b64_string

def get_access_token():
    token_url="https://accounts.spotify.com/api/token"
    payload={
        "grant_type":"client_credentials"
    }
    headers={
        "Authorization":f"Basic {get_base64_value(os.environ.get('client_id')+':'+os.environ.get('client_secret'))}",
        "Content-Type":"application/x-www-form-urlencoded"
        
    }

    response=requests.post(token_url,headers=headers,data=payload).json()
    return response['access_token']

def do_refresh_access_token():
    access_token=get_access_token()
    conn,cur=get_connection()
    #check whether the table is there or not
    cur.execute(check_whether_table_is_present_or_not.format(table_name='secrets'))
    r=cur.fetchall()
    if len(r) ==0:
        #table is not there and table should be created
        cur.execute(create_secrets_table)
        conn.commit()
    # check whether access_token key is there or not
    cur.execute("SELECT * FROM secrets WHERE secret_key='access_token'")
    r=cur.fetchall()
    if len(r)==0:
        # access_token key is not there
        cur.execute("INSERT INTO secrets (secret_key) VALUES('access_token')")
        conn.commit()
    #update the token
    cur.execute("UPDATE secrets SET secret_value='{}',updated_on=current_timestamp where secret_key='access_token'".format(access_token))
    conn.commit()
    cur.close()
    conn.close()
    




