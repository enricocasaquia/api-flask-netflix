import pandas as pd
import sqlite3

def escape_sql(value):
    if value == 'nan':
        return 'null'
    value = value.replace("'", "''")
    return f"'{value}'"

def convert_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%B %d, %Y').strftime('%Y-%m-%d')
    except Exception:
        return date_str

csv_file = 'netflix_titles.csv'
sql_file = 'migration.sql'
table_name = 'tb_movie'
instance = '../instance/movie.db'

dt = pd.read_csv(csv_file)

if 'data_added' in dt.columns:
    dt['data_added'] = dt['data_added'].apply(convert_date)

with open(sql_file, 'w', encoding='utf-8') as f_sql, sqlite3.connect(instance) as connection:
   try:
       cursor = connection.cursor()
   except sqlite3.Error as e:
        print(f'Database error: {e}')
   for i, row in dt.iterrows():
       columns = dt.columns.to_list()
       values = [escape_sql(str(convert_date(row[col]))) for col in columns]
       sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
       f_sql.write(sql)
       try:
           cursor.execute(sql)
       except sqlite3.Error as e:
           print(f'Database error: {e}')
