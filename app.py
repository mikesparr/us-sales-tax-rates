#!/usr/bin/env python

import flask
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

app = flask.Flask(__name__)

# override configs with env vars if available
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

# define routes
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/rate/<zipcode>")
def rate(zipcode):
    print ('zipcode: {}'.format(zipcode))

    try:
        # connect to database
        conn = pymysql.connect( 
            host=conf['db_host'], 
            user=conf['db_user'], 
            password=conf['db_pass'], 
            db=conf['db_name'] )

        # query the database
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM rate WHERE zip_code=%s", (zipcode) )

        # return result
        result = cursor.fetchone()
        print ('Result: ', result)

        # create rate dict
        rate = {
            'zip_code': result['zip_code'],
            'state_code': result['state'],
            'tax_region': result['tax_region_name'],
            'state_rate': float(result['state_rate']),
            'estimated_combined_rate': float(result['est_combined_rate']),
            'estimated_county_rate': float(result['est_county_rate']),
            'estimated_city_rate': float(result['est_city_rate']),
            'risk_level': float(result['risk_level'])
        }

        conn.close()

        return flask.jsonify( {'error': None, 'rate': rate} )

    except Exception as err:
        return flask.jsonify( {'error': str(err), 'rate': None} )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
