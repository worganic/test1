#!/usr/bin/python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

print ("log : Lancement du script Livebox V1")

liveboxIp = '90.73.108.422:8085';
url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key=116&mode=0';
    
@app.route('/webhook', methods=['POST'])
def webhook():
    
    print ("log : debut webhook")
    req = request.get_json(silent=True, force=True)
    
    print ("Lancement du script Livebox V1")
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    print ("log : debut makeWebhookResult")
    
    if req.get("queryResult").get("action") == "livebox-chaines":
        print ("log : debut req.get(result)")
        
        liveboxIp = '90.73.108.42:8085'
        url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key='
        result = req.get("queryResult")
        parameters = result.get("parameters")
        zone = parameters.get("chaines")
        zone1 = zone[0]

        cost = {'1':'TF1', '2':'France 2', '3':'France 3', '4':'Canal plus', '5':'France 5', '6':'M 6'}
        speech = "La chaîne " + str(cost[zone1]) + " va être lancé."
        
        zone2 = int(zone1)

        code = {0:'512', 1:'513', 2:'514', 3:'515', 4:'516', 5:'517', 6:'518', 7:'519', 8:'520', 9:'521'}

        unite = zone2 % 10
        dizaine = (zone2 % 100) / 10
        centaine = (zone2 % 1000) / 100
        
        if centaine > 0.9:
            codeA = code[centaine]
            url = url2 + codeA + '&mode=0'
            page = urllib.request.urlopen(url) 
            strpage = page.read()

        if dizaine > 0.9:
            codeA = code[dizaine]
            url = url2 + codeA + '&mode=0'
            page = urllib.request.urlopen(url) 
            strpage = page.read()

        codeA = code[unite]
        url = url2 + codeA + '&mode=0'
        page = urllib.request.urlopen(url) 
        strpage = page.read()
        
        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-worganic-livebox",
            "urlA": url 
        }
    elif req.get("result").get("action") == "Livebox-action":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("LActions")
        print(zone)
        print(zone[0])

        cost = {'act1':'116', 'act2':'116', 'act3':'352', 'act4':'139', 'act5':'115', 'act6':'114'}
        speech = "l'action à été lancé."
        
        if parameters.get("LActionPlus") == "actP2":#Diminuer le volume.
            code = cost['act6']
        elif parameters.get("LActionPlus") == "actP1":#Augmenter le volume.
            code = cost['act5']
        else:
            code = cost[zone[0]]

        liveboxIp = '90.73.151.42:8085'
        url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key='
        
        url = url2 + code + '&mode=0'
        page = urllib.request.urlopen(url) 
        strpage = page.read()
        
        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-worganic-livebox",
            "urlA": url 
        }
    else:
        return {}

@app.route('/')
def index():
    return "Retourne true pour appli livebox appel direct."

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port ")
    
    app.run(debug=True, port=port, host='0.0.0.0')
