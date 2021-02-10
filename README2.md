# Title
## Overview - What it does
## How to get it set up
To get started developing, first set up and activate a Python virtualenv, then install the dependencies using yarn and pip:

python3 -m env env
source env/bin/activate
pip3 install -r requirements.txt
yarn (??)
Now, you can run the application in two separate terminals. Start the Flask backend server:

flask run
And start the React frontend, which automatically sets up a proxy to the Flask server:

npm start
This should automatically open the application in your browser window. Both environments should automatically reload.


## Resources that inspired this
