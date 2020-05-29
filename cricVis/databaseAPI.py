import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('cricVis/static/cricVis/firebase-sdk.json')

firebase_admin.initialize_app(cred, {
	'databaseURL' : 'https://trial-1-9f3d9.firebaseio.com/'
})

ref = db.reference('/')
