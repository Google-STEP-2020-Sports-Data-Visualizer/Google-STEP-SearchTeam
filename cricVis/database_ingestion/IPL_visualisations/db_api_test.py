#Make a GET call to the database to check latency (in seconds) in retrieving data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import time
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

cred = credentials.Certificate("firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cricvis-1a59f.firebaseio.com/'
})

t1 = time()
cricVisDB_ref = db.reference("/")
t2 = time()
logging.info("Time to get cricVisDB_ref: ", t2-t1)

t3 = time()
match_description_ref = cricVisDB_ref.child("MatchDescription")
t4 = time()
logging.info("Time to get match_description_ref: ", t4-t3)

t5 = time()
match_description_dict = match_description_ref.get()
t6 = time()
logging.info("Time to get match_description_dict: ", t6-t5)

"""
Output (in seconds):
Time to get cricVisDB_ref:  0.00033593177795410156
Time to get match_description_ref:  7.3909759521484375e-06
Time to get match_description_dict:  2.1478004455566406
"""
