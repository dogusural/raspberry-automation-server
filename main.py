'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import datetime
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#define actuators GPIOs
ledRed = 13
ledYlw = 19
ledGrn = 26
#initialize GPIO status variables
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0
# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT) 
# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # returns a 200 (not a 404) with the following contents:
    return render_template('error.html')

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'selam cnm!',
      'time': timeString
      }
   return render_template('index.html', **templateData)
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
   if deviceName == 'red':
      actuator = ledRed
   elif deviceName == 'yellow':
      actuator = ledYlw
   elif deviceName == 'green':
      actuator = ledGrn
   else:
      templateData = {}
      return render_template('error.html', **templateData)
   if action == "on":
      GPIO.output(actuator, GPIO.HIGH)
   elif action == "off":
      GPIO.output(actuator, GPIO.LOW)
   else:
      templateData = {}
      return render_template('error.html', **templateData)

   ledRedSts = GPIO.input(ledRed)
   ledYlwSts = GPIO.input(ledYlw)
   ledGrnSts = GPIO.input(ledGrn)
   
   templateData = {
               'red'  : ledRedSts,
               'yellow'  : ledYlwSts,
               'green'  : ledGrnSts,
   }
   return render_template('action.html', **templateData)
@app.route("/control")
def control():
   ledRedSts = GPIO.input(ledRed)
   ledYlwSts = GPIO.input(ledYlw)
   ledGrnSts = GPIO.input(ledGrn)

   templateData = {
               'red'  : ledRedSts,
               'yellow'  : ledYlwSts,
               'green'  : ledGrnSts,
   }
   return render_template('action.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
