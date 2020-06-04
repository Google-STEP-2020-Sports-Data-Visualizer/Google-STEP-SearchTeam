from django.db import models
from firebase_admin import credentials, initialize_app, db
# Create your models here.
teamImageName = { 
    "Sunrisers Hyderbad": "../static/cricVis/SRH.png",
    "Mumbai Indians":"../static/cricVis/MI.png",
    "Gujarat Lions":"../static/cricVis/GL.png",
    "Rising Pune Supergiant":"../static/cricVis/RPS.png",
    "Royal Challengers Bangalore":"../static/cricVis/RCB.png",
    "Kolkata Knight Riders":"../static/cricVis/KKR.png",
    "Delhi Daredevils":"../static/cricVis/DD.png",
    "Kings XI Punjab": "../static/cricVis/KXIP.png",
    "Deccan Chargers":"../static/cricVis/DC.png",
    "Chennai Super Kings":"../static/cricVis/CSK.png",
    "Rajasthan Royals": "../static/cricVis/RR.png"}

cred = credentials.Certificate('cricVis/static/cricVis/cricvistesting-firebase-adminsdk-b4xg8-af8c48bb20.json')

initialize_app(cred, {
	'databaseURL' : 'https://cricvistesting.firebaseio.com/'
})