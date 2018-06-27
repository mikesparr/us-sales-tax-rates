#!/usr/bin/env python

import csv
import os
import pymysql

# get default env configs
conf = {
    'db_host': 'localhost',
    'db_port': 3306,
    'db_name': 'tax_rates',
    'db_user': 'user_tax',
    'db_pass': 'unclesam'
}

def load_env():
    try:
        env_conf = {
            'db_host': os.environ['TAX_RATES_DB_HOST'],
            'db_port': int(os.environ['TAX_RATES_DB_PORT']),
            'db_name': os.environ['TAX_RATES_DB_NAME'],
            'db_user': os.environ['TAX_RATES_DB_USER'],
            'db_pass': os.environ['TAX_RATES_DB_PASS']
        }
        conf.update(env_conf)
    except KeyError:
        print ("Missing environment variables so using default")

'''
Database fields
state, zip_code, tax_region_name, state_rate, est_combined_rate, est_county_rate, est_city_rate, est_special_rate, risk_level
'''
def load_files():
    try:
        # connect to database
        conn = pymysql.connect( 
            conf['db_host'], 
            conf['db_user'], 
            conf['db_pass'], 
            conf['db_name'] )

        # prepare a cursor object using cursor() method
        cursor = conn.cursor()

        # prepare query
        insert_query = '''
            INSERT INTO rate (state, zip_code, tax_region_name, 
                state_rate, est_combined_rate, est_county_rate, 
                est_city_rate, est_special_rate, risk_level) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        # load files in dir and insert into database
        for root, dirs, files in os.walk('./data/TAXRATES_ZIP5'):
            for file in files:
                with open('./data/TAXRATES_ZIP5/{}'.format(file), 'r') as f:
                    reader = csv.reader(f)
                    next(reader) # skip header row
                    for row in reader:
                        cursor.execute(insert_query, row)
        
        # commit to db and close up
        conn.commit()
        conn.close()
    except Exception as err:
        print ('Error loading files into database: ', err)


def main():
    print ('Loading ENV config...')
    load_env()
    print ('Loading CSV files...')
    load_files()

if __name__ == '__main__': main()
