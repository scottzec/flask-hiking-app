from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import weather_api
from datetime import datetime, timezone
# from dotenv import load_dotenv
# import os

# load_dotenv()

app = Flask(__name__) # I create an instance of Flask I can use here
cors = CORS(app) #initializes CORS

# config.py file is better way to later connect db where all variables will live
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///login_users' # SWITCH TO DEPLOYED DB

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ndkkehfxwfrhwx:8e9dcf6bf7d646cfed08f429670580fd545233e6df9ea58ac35783963aaceb30@ec2-34-230-167-186.compute-1.amazonaws.com:5432/d620dgs57jjv59'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# helps models/schemas to migrate in sql
migrate = Migrate(app, db)

# init marshmallow app
marsh = Marshmallow(app)

# USER MODEL, inherits class from SQLAlchemy parent class. User will be child of model class
class User(db.Model): 
    id = db.Column(db.Integer, primary_key = True) # would autogenerate postsql, but python needs it to be defined
    username = db.Column(db.String)
    password = db.Column(db.String)
    regions = db.relationship('Region', backref='user')

    # Constructor: initialization function triggered when we create an instance
    # def __init__ (self, username, password, regions = []): added regions for 2nd table

    def __init__ (self, username, password): #ADD REGIONS=[] here??
        # self.id = id #postgres creates it for me automatically apparently
        self.username = username
        self.password = password


    def __repr__(self): # offical way to represent string when we call it
        return '<id {}>'.format(self.id)

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String) #, nullable=False ??

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #nullable=False?

    def __init__ (self, region_name, user):
        # self.id = id shouldnt need it
        self.region_name = region_name
        self.user_id = user

    def __repr__(self): # offical way to represent string when we call it
        return '<id {}>'.format(self.id)

class UserSchema(marsh.Schema):
    class Meta: # describes the data fields we need
        fields = (
            'id',
            'username',
            'password'
        )

user_schema = UserSchema() #reference to UserSchema class
users_schema = UserSchema(many=True)

class RegionSchema(marsh.Schema):
    class Meta: # describes the data fields we need
        fields = (
            'id',
            'region_name',
            'user_id'
        )

region_schema = RegionSchema() #reference to RegionSchema class
regions_schema = RegionSchema(many=True)


# WEATHER LOOK-UP
def lookup_weather(lat,lon):
    weather = weather_api.fetch_weather(lat,lon)
    return weather
    

# ROUTES

@app.route('/api/user', methods=['POST'])
@cross_origin() #anytime we go to this route, satisfy the cross origin
def add_user():
    username = request.json['username']
    password = request.json['password']

    # sqlalchemy, looks up user in the db 
    user = User.query.filter(User.username==username, User.password==password).first()

    if user:
        return user_schema.jsonify(user)

    new_user = User(username, password) 

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/api/region', methods=['POST'])
@cross_origin() #anytime we go to this route, satisfy the cross origin
def add_region():
    region_name = request.json['region_name']
    user_id = request.json['user_id']


    # Shouldn't be necesary for region: sqlalchemy, looks up user in the db 
    # region = Region.query.filter(Region.region_name==region_name, Region.user_id==user_id).first()
    # if region:
    #     return region_schema.jsonify(region)

    new_region = Region(region_name, user_id) 

    db.session.add(new_region)
    db.session.commit()

    return region_schema.jsonify(new_region)

@app.route('/api/users', methods=['GET'])
@cross_origin()
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/api/regions', methods=['GET'])
@cross_origin()
def get_regions():
    all_regions = Region.query.all()
    result = regions_schema.dump(all_regions)
    return jsonify(result)

# ROUTE RETURNS REGIONS ASSIGNED TO A USER ID
@app.route('/api/regions/<user_id>/', methods=['GET'])
@cross_origin()
def get_regions_user(user_id):
    regions_user = Region.query.filter(Region.user_id==user_id)
    print(regions_user)

    if regions_user:
        return regions_schema.jsonify(regions_user)

    return jsonify(result)

# CREATE ROUTE TO PATCH A USER's REGIONS, OR DELETE?





# GET request is default in flask, any other one needs to be specified
@app.route('/weather/<region>')
@cross_origin()
def get_weather_region(region):

    rainier_weather = (lookup_weather(46.7853,-121.7353718))
    day = "Today"
    #NIGHTMARE converting UTC, find workaround: date = utc_to_local(str((rainier_weather["daily"][0]["dt"])))
    day_temp = str(rainier_weather["daily"][0]["feels_like"]["day"])
    forecast = str(rainier_weather["daily"][0]["weather"][0]["main"])
    icon = str(rainier_weather["daily"][0]["weather"][0]["icon"])
    rainier_dict = { "region": "Tahoma", "day": day, "temp": day_temp, "weather": forecast, "icon": icon }
    
    mntn_loop_weather = (lookup_weather(48.088049, -121.389147))
    day = "Today"
    day_temp = str(mntn_loop_weather["daily"][0]["feels_like"]["day"])
    forecast = str(mntn_loop_weather["daily"][0]["weather"][0]["main"])
    icon = str(mntn_loop_weather["daily"][0]["weather"][0]["icon"])
    mntn_loop_dict = { "region": "Mountain Loop Highway", "day": day, "temp": day_temp, "weather": forecast, "icon": icon }

    if region=="tahoma":
        return jsonify(rainier_dict)
    elif region=="mntnloop":
        return jsonify(mntn_loop_dict)
    else:
        return "No weather"

@app.route('/')
def welcome():
    return "Hiking Weather App Incoming"
    # rainier_weather = (lookup_weather(46.7853,-121.7353718))
    # day = "Today"
    # #NIGHTMARE converting UTC, find workaround: date = utc_to_local(str((rainier_weather["daily"][0]["dt"])))
    # day_temp = str(rainier_weather["daily"][0]["feels_like"]["day"])
    # forecast = str(rainier_weather["daily"][0]["weather"][0]["main"])
    # icon = str(rainier_weather["daily"][0]["weather"][0]["icon"])
    # rainier_dict = { "region": "Tahoma", "day": day, "temp": day_temp, "weather": forecast, "icon": icon }
    
    # mntn_loop_weather = (lookup_weather(48.088049, -121.389147))
    # day = "Today"
    # day_temp = str(mntn_loop_weather["daily"][0]["feels_like"]["day"])
    # forecast = str(mntn_loop_weather["daily"][0]["weather"][0]["main"])
    # icon = str(mntn_loop_weather["daily"][0]["weather"][0]["icon"])
    # mntn_loop_dict = { "region": "Mountain Loop Highway", "day": day, "temp": day_temp, "weather": forecast, "icon": icon }

    # weather_list_of_dicts = [
    #     rainier_dict,
    #     mntn_loop_dict
    # ]

    # return jsonify(weather_list_of_dicts)

# optional condition that makes sure you are running appropriate server file
if __name__ == '__main__':
    app.run(debug=True) #remove for production, development only

