'''
Code created by Matt Richardson 
for details, visit:  http://mattrichardson.com/Raspberry-Pi-Flask/inde...
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect
import datetime
import monitor

def readGpioInput(pinNumber):
   status = GPIO.input(pinNumber)
   return ("ON" if status == 1 else "OFF") 

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
      'title' : 'Home',
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
      return render_template('error.html')
   if action == "on":
      GPIO.output(actuator, GPIO.HIGH)
   elif action == "off":
      GPIO.output(actuator, GPIO.LOW)
   else:
      return render_template('error.html')

   ledRedSts = readGpioInput(ledRed)
   ledYlwSts = readGpioInput(ledYlw)
   ledGrnSts = readGpioInput(ledGrn)
   templateData = {
               'red'  : ledRedSts,
               'yellow'  : ledYlwSts,
               'green'  : ledGrnSts,
   }
   return redirect('control')

@app.route("/control")
def control():
   ledRedSts = readGpioInput(ledRed)
   ledYlwSts = readGpioInput(ledYlw)
   ledGrnSts = readGpioInput(ledGrn)

   templateData = {
               'red'  : ledRedSts,
               'yellow'  : ledYlwSts,
               'green'  : ledGrnSts,
   }
   return render_template('action.html', **templateData)


@app.route('/monitor')
def index():
	return render_template('monitor.html', 
                           fahrenheit=monitor.getFahrenheit(),
                           celsius=monitor.getCelsius(),
                           diskUsageHeader=monitor.getDiskUsage(0), # array for Disk Usage <th>
                           diskUsageInfo=monitor.getDiskUsage(1), # array for Disk Usage <td>
                           upTime=monitor.getUptime(), # how long the raspberry pi has been running
                           memoryUsageHeader=monitor.getMemoryUsage(0), # array for Memory Usage <th>
                           memoryUsageInfo=monitor.getMemoryUsage(1), # array for Memory Usage <td>
                           memoryUsePercentage=round(float(monitor.getMemoryUsage(1)[2]) / float(monitor.getMemoryUsage(1)[1]), 4) * 100, # percentage of used Memory
                           ipAddress=monitor.getIpAddress()[0],
                           processInfo=monitor.getProcessInfo()
                          )

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

def readGpioInput(pinNumber):
   status = GPIO.input(pinNumber)
   return ("ON" if 1 else "OFF") 
