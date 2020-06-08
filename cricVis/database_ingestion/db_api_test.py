import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pprint

cred = credentials.Certificate("firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cricvis-1a59f.firebaseio.com/'
})

ref = db.reference("/")
x = ref.child("MatchDescription")
matref = x.get()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(matref)
