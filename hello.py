# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
import json
import datetime
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/alexa_end_point', methods=['POST'])
def alexa():
    print("dans alexa__________________________________")
    event = request.get_json()
    print (event)
    req = event['request']
    

    if req['type'] == 'LauchRequest':
        print('dans lauch')
        return handle_launch_request()
    elif req['type'] == 'IntentRequest':
        print('dans intent')
        if req['intent']['name'] == 'helloIntent':
            return handle_hello_intent(req)
        else:
            return "mais que se passe-til?", 400
    elif req['type'] == "SessionEndedRequest":
        pass

def handle_hello_intent(req):
    name = req['intent']['slots']['FirstName']['value']
    res = Response()
    res.speech_text = 'Bonjour <say-as-interpret-as="spell-out">{0}</say-as>{0}.'.format(name)
    res.speech_text += get_wish()
    return res.build_response()

def get_wish():
    current_time = datetime.datetime.utcnow()
    hours = current_time.hour + 1
    if hours < 0:
        hours = 24 + hours
    if hours < 12:
        return "Passez une bonne matinée"
    elif hours < 18:
        return "Passez une agréable après-midi"
    else:
        return "Passez une bonne soirée"

def handle_launch_request():
    'Handles lauch request and generate response'
    res = Response()
    res.speech_text = 'Bienvenu dans le test d\'utilisation d\'une API Flask comme point sortie'
    res.reprompt_text = "Pas de text de répétition"
    res.end_session = False
    return res.build_response()
class Response(object):
    'Alexa skill response object with helper function'

    def __init__(self):
        self.speech_text    = None
        self.reprompt_text  = None
        self.end_session    = True
    def build_response(self):
        'Build Alexa response and return'

        final_response = {
            'version' : '1.0', 
            'response' : {
                'outputSpeech': {
                    'type' : 'SSML', 
                    'ssml' : '<speak>' + self.speech_text + '</speak>'
                }, 
                'shouldEndSession' : self.end_session
            }
        }

        if self.reprompt_text:
            final_response['response']['reprompt_text'] = {
                'outputSpeech': {
                    'type' : 'SSML', 
                    'ssml' : '<speak>' + self.reprompt_text + '</speak>'
                }
            }
        print('Dans la response_________________________________')
        print (final_response)
        http_response = make_response(json.dumps(final_response))
        http_response.headers['Content-Type'] = 'application/json'
        return http_response

if __name__ == "__main__":
    # app.debug = True
    # app.run()
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')