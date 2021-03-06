# appJSON.py
#   purp: to accept JSON strings from an input and interpret get and set requests;
#       uses wrapper functions to call ev3dev functions on linux system
#   created by: Juliana Furgala
#   notes: has less implemented functions than the newer appJSON.py
#   last edited on: August 3, 2016 for updating comments

# tutorial for set-up found here: https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet/
from flask import Flask, render_template, request, json
from flask_cors import CORS, cross_origin
from ev3dev import *
import ev3dev.ev3 as ev3
import logging, time
from ev3dev.auto import list_motors
# import tweepy

PYTHONIOENCODING = 'utf-8'  # set the language to standard English characters (in case your system isn't)

app = Flask(__name__)
# basic logging, tells you when you have received a request ('GET'/'POST', etc.)
logging.basicConfig(level=logging.INFO)

# advanced debugging log, to use, uncomment line below
# logging.getLogger('flask_cors').level = logging.DEBUG

# resources = what pages you want to have access allowed to, can be 1 page, in this case is '/' (home page)
# origin = the list of allowed IP addresses to connect, your own is already allowed
# methods = what can the user/person do to the page(s)
CORS(app, resources=r'/*', origin="http://130.64.94.22:8888/", methods=["GET", "POST"])


# Inspiration for methods parameter and if method == format
# https://github.com/distortenterprises/Webinterface
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        JSONinput = request.get_data()

#        print("Command received")
        data = json.loads(JSONinput)
#        print(
#            "status is ", data['status'], " and io_type is", data['io_type'], " and port is ", data['port'], " and info is ", data['info'], " and value is ", data['value'], " and mode is ", data['mode'])
        # status, io_type, info, mode are used for get and set
        # status is get/set, io_type is input/output type,
        # info is the function you want called, mode is the
        # units or mode you want to get back / set 
        # value parameter is used for set only, to send an int
        requesteddata = str(process_command(data))
        return json.jsonify(httpCode=200, value=requesteddata)

    elif request.method == "GET":
        # return render_template('index.html')
        return "Successful get request"


def process_command(data):
    status = data['status']
    io_type = data['io_type']
    
    result = "Not found"
    if status == 'get':
        if io_type == 'touch':
            result = get_touch(data['port'], data['info'])
        if io_type == 'ultrasonic':
            result = get_ultrasonic(data['port'], data['info'], data['mode'])
        if io_type == 'color':
            result = get_color(data['port'], data['info'], data['mode']) 
        if io_type == 'large motor' or io_type == 'medium motor':
            result = get_motor(data['io_type'], data['port'], data['info'], data['mode'])
    if status == 'set':
        if io_type == 'large motor' or io_type == 'medium motor':
            result = set_motor(data['io_type'], data['port'], data['info'], data['value'])
        if io_type == 'sound':
            result = set_sound(data['value'], data['mode'])
        if io_type == 'led':
            result = set_led(data['info'], data['value'], data['mode'])
        if io_type == 'twitter':
            # result = set_twitter_post(data['port'], data['info'], data['value'])
            result = 'theoretically sending a tweet'
    return result


# get_touch
#   purp: to return the current value from a touch sensor
def get_touch(port, info):
    try:
        if info == 'value':
            return ev3.TouchSensor(port).value()
    except ValueError:
        return "Not found"


# get_ultrasonic (US)
#   purp: to return the current value of a US in cm or in
def get_ultrasonic(port, info, mode):
    try:
        if info == 'value':
            if mode == 'cm':
                return ev3.UltrasonicSensor(port).value()*0.1
            if mode == 'in':
                return ev3.UltrasonicSensor(port).value()*0.1*0.393701
    except ValueError:
        return "Not found"


# get_color
#   purp: to return the current value of the color sensor in a certain mode;
#       has ambient, reflected, color recognition modes, etc.
def get_color(port, info, mymode):
    try:
        if info == 'value':
            ev3.ColorSensor(port).mode(mymode)
            return ev3.ColorSensor(port).value()
    except ValueError:
        return "Not found"


# get_motor
#   purp: to return a value/stat from a motor
def get_motor(io_type, port, info, mode):
    try:
        if io_type == 'large motor':
            i = ev3.LargeMotor(port)
        elif io_type == 'medium motor':
            i = ev3.MediumMotor(port)

        if info == 'position':
            if mode == 'rotations':
                return i.position()/i.count_per_rot()
            elif mode == 'degrees':
                return i.position()
        if info == 'duty_cycle':
            return i.duty_cycle()
        if info == 'speed':
            return i.speed()
    except ValueError:
        return "Not found"


# set_motor
#   purp: to run a function for a motor with given values
def set_motor(io_type, port, info, value):
    try:
        if io_type == 'large motor':
            i = ev3.LargeMotor(port)
        elif io_type == 'medium motor':
            i = ev3.MediumMotor(port)
        power = int(value)
        if info == 'run forever':
            i.run_forever(duty_cycle_sp=power)
            time.wait(1)
        # if info == 'run_timed':
        #    i.run_timed(time_sp=timer, duty_cycle_sp=power)
        if info == 'stop':
            i.stop(stop_action=value)
        if info == 'reset':
            i.reset()
        if info == 'switch':
            i.duty_cycle_sp(i.duty_cycle_sp * -1)
        if info == 'stop all':
            # credit for the following two lines goes to dwalton76 : https://github.com/rhempel/ev3dev-lang-python/blob/develop/utils/stop_all_motors.py
            for motor in list_motors():
                motor.stop(stop_action=value)
    except ValueError:
        return "Not found"
    

# set_sound
#   purp: to emit a chosen sound
def set_sound(value, mode):
    try:
        if mode == 'tone':
            ev3.Sound.tone(value)
        if mode == 'beep':
            ev3.Sound.beep(value)
        if mode == 'file':
            ev3.Sound.play(value)
        if mode == 'speech':
            ev3.Sound.speak(value)
        return "successful set"
    except ValueError:
        return "Not found"


# set_led
#   purp: to set the colors of the LEDs behind the brick buttons;
#       mode (which side) = left, right, both
def set_led(info, value, mode):
    try:
        if info == 'on':
            if mode == 'left':
                if value == 'green':
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
                if value == 'red':
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                if value == 'yellow':
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
                if value == 'amber':
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
            if mode == 'right':
                if value == 'green':
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
                if value == 'red':
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                if value == 'yellow':
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
                if value == 'amber':
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.AMBER)
            if mode == 'both':
                set_led(info, value, 'left')
                set_led(info, value, 'right')
            
        elif info == 'off':
            if mode == 'left':
                ev3.Leds.off(ev3.Leds.LEFT)
            if mode == 'right':
                ev3.Leds.off(ev3.Leds.RIGHT)
            if mode == 'both':
                ev3.Leds.all_off()
        return "successful set"
    except ValueError:
        return "Not found"


# set_twitter_post
    #  information for this demo function and code outline came from an online tutorial at:
    # nodotcom.org/python-twitter-tutorial.html
def set_twitter_post(port, info, value):
    try:
        def get_api(cfg):
            auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
            auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
            return tweepy.API(auth)

        consumer_key, consumer_secret, access_token, access_token_secret = port.split(':')
        cfg = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret
        }

        api = get_api(cfg)

        if info == 'post':
            status = api.update_status(status=value)  # value = your message
            print(status)
    except ValueError:
        return "Not found"
    

# needs to be fixed; wants to JSON parse a form...
# To be: a locally hosted page that takes in form data and responds to commands
@app.route('/1', methods=["GET", "POST"])
def index1():
    if request.method == "POST":
        if request.form['direction'] == 'forward':
            m.run_forever(duty_cycle_sp=40)
        if request.form['direction'] == 'backward':
            m.run_forever(duty_cycle_sp=-40)
        if request.form['direction'] == 'stop':
            m.stop()
        print("Command received")
        print(request.form['direction'])
        return render_template('index.html')
    if request.method == "GET":
        return render_template('index.html')


# error handling for broad server and client issues
@app.errorhandler(400)  # client-side error; something wrong with client browser/interface
def client_error(error):
    app.logger.error('Client Error: %s', error)
    return ('{httpCode: %s}', error)


@app.errorhandler(500)  # server-side error; something wrong with the brick's server
def internal_server_error(error):
    app.logger.error('Server Error: %s', error)
    return ('{httpCode: %s}', error)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
