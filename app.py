#!/usr/bin/python

import time
import sys

# Flask app should start in global layout
app = Flask(__name__)

print ("Script python test.py 2 ....")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
