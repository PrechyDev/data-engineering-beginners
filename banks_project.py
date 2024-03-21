#exchange rate csv file to be downloaded - https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv
#install pandas and bs4 libraries

import pandas as pd 
import numpy as np 
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
initial_attr = ['Name', 'MC_USD_Billion']
#final_attr = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
csv_path = './Largest_banks_data.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'
logfile = 'code_log.txt'

def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(logfile,"a") as f: 
        f.write(timestamp + ' : ' + message + '\n')

def extract(url, initial_attr):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''

    df = pd.DataFrame(columns=initial_attr)
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')
        #remove \n and add to dict
        if len(col) != 0:
            data_dict = {"Name": col[1].text.replace('\n', ''), 
                            "MC_USD_Billion": float(col[2].contents[0].replace('\n', ''))}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
        
    return df


def transform(df):
    ''' This function transform the dataframe 
    by adding columns for Market Capitalization in GBP, EUR and INR, rounded to 2 decimal places,
     based on the exchange rate information shared as a CSV file.'''
    
    #to get exchange rate
    rate = pd.read_csv('exchange_rate.csv')
    eur = rate.loc[rate['Currency'] == 'EUR', 'Rate'].values[0]
    gbp = rate.loc[rate['Currency'] == 'GBP', 'Rate'].values[0]
    inr = rate.loc[rate['Currency'] == 'INR', 'Rate'].values[0]

    #getting new lists
    MC_USD = df["MC_USD_Billion"].tolist()
    MC_EUR = [np.round(x*eur, 2) for x in MC_USD]
    MC_GBP = [np.round(x*gbp, 2) for x in MC_USD]
    MC_INR = [np.round(x*inr, 2) for x in MC_USD]
    
    #appending new lists to dataframe
    df["MC_EUR_Billion"] = MC_EUR
    df["MC_GBP_Billion"] = MC_GBP
    df["MC_INR_Billion"] = MC_INR

    return df

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''

    df.to_csv(csv_path)

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

# Log process
log_progress('Preliminaries complete. Initiating ETL process')

extracted_data = extract(url, initial_attr)
print(extracted_data)
log_progress('Data extraction complete. Initiating Transformation process')
 
transformed_data = transform(extracted_data) 
print(transformed_data)
log_progress('Data transformation complete. Initiating loading process')

load_to_csv(transformed_data, csv_path) 
log_progress('Data saved to CSV file')

conn = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')
 
load_to_db(transformed_data, conn, table_name)
log_progress('Data loaded to Database as table. Executing queries')
 
query_all = f'SELECT * FROM {table_name}'
run_query(query_all, conn)

query_avg = f'SELECT AVG(MC_GBP_Billion) FROM Largest_banks'
run_query(query_avg, conn)

query_top5 = f'SELECT Name from Largest_banks LIMIT 5'
run_query(query_top5, conn)

log_progress('Process Complete.')

#close sqlite3 connection
conn.close()
log_progress('Server Connection closed')
