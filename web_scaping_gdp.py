import pandas as pd 
import numpy as np 
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
target_file = 'Countries_by_GDP.csv'
logfile = 'etl_project_log.txt'
table_name = 'Countries_by_GDP'
db_name = 'World_Economies.db'
attr_list = ['Country', 'GDP_USD_millions']

def extract(url, attr_list):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''

    df = pd.DataFrame(columns=attr_list)
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')

    for row in rows:
        col = row.find_all('td')

        if len(col) != 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0], 
                            "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)

    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''
    
    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000, 2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    return df

def load_to_csv(df, target_file):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''

    df.to_csv(target_file)

def load_to_db(df, conn, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def run_query(query, conn):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query)
    query_output = pd.read_sql(query, conn)
    print(query_output)

def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(logfile,"a") as f: 
        f.write(timestamp + ' - ' + message + '\n')

# Log process
log_progress('Preliminaries complete. Initiating ETL process')

extracted_data = extract(url, attr_list) 

log_progress('Data extraction complete. Initiating Transformation process')
 
transformed_data = transform(extracted_data) 

log_progress('Data transformation complete. Initiating loading process')

load_to_csv(transformed_data, target_file) 

log_progress('Data saved to CSV file')

conn = sqlite3.connect(db_name)

log_progress('SQL Connection initiated.')
 
load_to_db(transformed_data, conn, table_name)

log_progress('Data loaded to Database as table. Running the query')
 
query = f'SELECT * FROM {table_name} WHERE GDP_USD_billions > 100'
run_query(query, conn)

log_progress('Process Complete.')

#close sqlite3 connection
conn.close()

