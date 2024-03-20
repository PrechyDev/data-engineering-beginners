import sqlite3
import pandas as pd 

conn = sqlite3.connect('STAFF.db')
table_name = 'INSTRUCTOR'
attr_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']

#CSV file - wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/INSTRUCTOR.csv
file_path = '/home/project/INSTRUCTOR.csv'
df = pd.read_csv(file_path, names = attr_list)
#print(df)

df.to_sql(table_name, conn, if_exists='replace', index=False)
print('Table is ready')

#view the table
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#display the number of rows/entries in the table
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#appending a new entry
data_dict = {'ID' : [100],
            'FNAME' : ['John'],
            'LNAME' : ['Doe'],
            'CITY' : ['Paris'],
            'CCODE' : ['FR']}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists='append', index=False)
print('Data appended successfully')


#New table - Departments
#csv file - https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/Departments.csv
dept_table = 'DEPARTMENTS'
dept_attrs = ['DEPT_ID', 'DEP_NAME', 'MANAGER_ID', 'LOC_ID']

dept_file = '/home/project/Departments.csv'
df = pd.read_csv(dept_file, names = dept_attrs)

df.to_sql(dept_table, conn, if_exists='replace', index=False)
print('Department table created')

#Append new entry to department
data = {'DEPT_ID': [9], 
        'DEP_NAME': ['Quality Assurance'], 
        'MANAGER_ID': [30010], 
        'LOC_ID':['L0010']}
new_entry = pd.DataFrame(data)
new_entry.to_sql(dept_table, conn, if_exists='append', index=False)

#view the table
query_statement = f"SELECT * FROM {dept_table}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#display the number of rows/entries in the table
query_statement = f"SELECT COUNT(*) FROM {dept_table}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#close connection
conn.close()
