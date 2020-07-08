from firebase_admin import credentials, initialize_app, db
cred = credentials.Certificate('static/cricVis/comparisonFirebaseSDK.json')

comparisonDB = initialize_app(cred, {
	'databaseURL' : 'https://playercomparison-6dde2.firebaseio.com/',
},name="comparisonDB")

refComparison = db.reference('/',comparisonDB)
