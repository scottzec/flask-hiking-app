from flask import Flask
app = Flask(__name__)


@app.route('/')
def hiking_weather():
    return "Hiking Weather App Incoming"

if __name__ == '__main__':
    app.run()