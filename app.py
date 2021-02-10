from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import weather_api
from datetime import datetime, timezone



app = Flask(__name__) # I create an instance of Flask I can use here
cors = CORS(app) #initializes CORS

# config.py file is better way to later connect db where all variables will live
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather_users'
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
    name = db.Column(db.String)
    email = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    # region1 = db.Column('region1', db.String) How to from limited list?

    # Constructor: initialization function triggered when we create an instance
    def __init__ (self, name, email, zipcode):
        self.name = name
        self.email = email
        self.zipcode = zipcode
        # self.region1 = region1
        # self.region2 = region2

    def __repr__(self): # offical way to represent string when we call it
        return '<id {}>'.format(self.id)

class UserSchema(marsh.Schema):
    class Meta: # describes the data fields we need
        fields = (
            'id',
            'name',
            'email',
            'zipcode'
        )

user_schema = UserSchema() #reference to UserSchema class
users_schema = UserSchema(many=True)





@app.route('/api/user', methods=['POST'])
@cross_origin() #anytime we go to this route, satisfy the cross origin
def add_user():
    name = request.json['name']
    email = request.json['email']
    zipcode = request.json['zipcode']

    new_user = User(name, email, zipcode)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/api/users', methods=['GET'])
@cross_origin()
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

def lookup_weather(lat,lon):
    weather = weather_api.fetch_weather(lat,lon)
    return weather

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

# GET request is default in flask, any other one needs to be specified
@app.route('/')
def welcome():
    # return "Hiking Weather App Incoming"
    rainier_weather = (lookup_weather(46.7853,-121.7353718))
    day = "Today"
    #NIGHTMARE converting UTC, find workaround: date = utc_to_local(str((rainier_weather["daily"][0]["dt"])))
    day_temp = str(rainier_weather["daily"][0]["feels_like"]["day"])
    forecast = str(rainier_weather["daily"][0]["weather"][0]["main"])
    icon = str(rainier_weather["daily"][0]["weather"][0]["icon"])
    rainier_dict = { "region": "Rainier", "day": day, "temp": day_temp, "weather": forecast, "icon": icon }
    
    mntn_loop_weather = (lookup_weather(48.088049, -121.389147))
    day = "Today"
    day_temp = str(mntn_loop_weather["daily"][0]["feels_like"]["day"])
    forecast = str(mntn_loop_weather["daily"][0]["weather"][0]["main"])
    icon = str(mntn_loop_weather["daily"][0]["weather"][0]["icon"])
    mntn_loop_dict = { "region": "Rainier", "day": day, "temp": day_temp, "weather": forecast, "icon": icon }

    weather_list_of_dicts = {
        "Tahoma": rainier_dict,
        "Mountain Loop Highway": mntn_loop_dict
    }

    return weather_list_of_dicts


# @app.route('/weather')
# def getWeather():
#     """ Weather web service """
#     location = request.args.get("location", None)
#     return lookupWeather(location)
    

# @app.route('/browse', methods=["GET"])
# def weather():
#     return jsonify({"region": "Snoqualmie"})

# optional condition that makes sure you are running appropriate server file
if __name__ == '__main__':
    app.run(debug=True) #remove for production, development only






