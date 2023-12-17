import pandas as pd
import psycopg2 as dbapi
import os, sys
import argparse
import numpy as np 
from datetime import datetime
import bcrypt

# custom modules
import config


def check_password(encrypted_password, plain_input_password):
    # Check if a password matches the hashed password
    return bcrypt.checkpw(plain_input_password.encode('utf-8'), encrypted_password)

def err_handler(err):
    print ("Exception has occured:", err)
    print ("Exception type:", type(err))
    err_type, err_obj, traceback = sys.exc_info()
    if traceback != None:
        line_num = traceback.tb_lineno
        fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
        print(f"in {fname}")
    else: line_num = "not found"
    print ("\nERROR:", err, "on line number:", line_num)
    print ("traceback:", traceback, "-- type:", err_type)

def db_connect(DSN):
    try:
        conn = dbapi.connect(DSN)
        return conn
    except os.error:
        err_handler(os.error)

input_format = "%d/%m/%Y %I:%M:%S %p"
def convert_datestyle(timestamp_str):
    # timestamp_str: Input timestamp string
    # Define the format of the input timestamp string

    # Convert the string to a datetime object
    dt_obj = datetime.strptime(timestamp_str, input_format)

    # Convert to PostgreSQL timestamp format and return 
    return dt_obj.strftime("%Y-%m-%d %H:%M:%S")


def execute_query(query, DSN):
    conn = None
    cur = None
    try:
        conn = dbapi.connect(DSN)
        cur = conn.cursor()
        cur.execute(query)
    except dbapi.errors.UniqueViolation:
        print("log already inserted")
    except os.error:
        err_handler(os.error)
    finally:
        if cur != None:
            cur.close()
            conn.commit()
            conn.close()
            