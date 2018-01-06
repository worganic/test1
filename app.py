#!/usr/bin/python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

print ("Script python test.py 2 ....")

@app.route('/')
def index():
    return "To conquer the human civilization on the other side."

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port ")
    
    app.run(debug=True, port=port, host='0.0.0.0')
