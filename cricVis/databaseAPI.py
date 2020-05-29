import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('static/firebase-sdk.json')

firebase_admin.initialize_app(cred, {
	'databaseURL' : 'https://trial-1-9f3d9.firebaseio.com/'
})

ref = db.reference('/')
match_ref = ref.push({
	'ID': '211',
	'CumulativeRuns': '213',
	'Over' : '22'
})

print(match_ref.key)
