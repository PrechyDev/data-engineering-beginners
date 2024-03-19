#install pandas library to start using pip install pandas
#download necessary files by running the code below in the terminal
#wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/datasource.zip 
#unzip file using unzip datasource.zip

import pandas as pd 
import glob
from datetime import datetime
import xml.etree.ElementTree as ET

#filenames for storing data and for tracking logs
target_file = 'transformed_data.csv'
logfile = 'logfile.txt'

def extract_from_csv(file):
   '''Function extracts csv file and save it to a pandas dataframe.'''
    df = pd.read_csv(file)
    return df

def extract_from_json(file):
 '''Function extracts data from json file and save it to a pandas dataframe.'''
    df = pd.read_json(file, lines=True)
    return df 

def extract_from_xml(file):
    '''
    Function parses xml file, iterates through each line and get the data need. 
    Then concat them into the pandas dataframe created in the first line.
    '''
    df = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    tree = ET.parse(file)
    root = tree.getroot()

    for car in root:
        car_model = car.find('car_model').text
        year_of_manufacture = car.find('year_of_manufacture').text
        price = float(car.find('price').text)
        fuel = car.find('fuel').text
        #add each data to a dict and append dict to df
        df = pd.concat([df, pd.DataFrame([{'car_model': car_model, 'year_of_manufacture':year_of_manufacture, 'price':price, 'fuel':fuel}])], ignore_index=True)
    return df

def extract():
   '''
    function searches for each file format and extracts it using 
    the glob function and the extraction function created for each file.
    '''

    #create empty dataframe to append data from files
    extracted_data = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
     
    # process all csv files 
    for csvfile in glob.glob("*.csv"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True) 
         
    # process all json files 
    for jsonfile in glob.glob("*.json"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True) 
     
    # process all xml files 
    for xmlfile in glob.glob("*.xml"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True) 
         
    return extracted_data 

def transform(data):
    '''function rounds price to 2 decimal places.'''
    data['price'] = round(data.price,2)
    return data

def load(target_file,transformed_data):
    '''function saves transformed data to target file.'''
    transformed_data.to_csv(target_file)
    
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(logfile,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 

# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 
