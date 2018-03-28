

from flask import Flask
from flask_googlemaps import GoogleMaps
app = Flask(__name__)
from app import views

GoogleMaps(app, key="AIzaSyBUgHP1nB5Nsm9k8IELrBRMpSSueJYA0r4")
