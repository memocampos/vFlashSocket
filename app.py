import flask
from flask import Flask, render_template,request
from flask_socketio import SocketIO,emit,namespace
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('event', namespace='/test')
def event(json):
    print("Received message: " + json)
    print(flask.request.sid)
    emit('event', json)
    #time.sleep(3)
    #emit('event', "true")
    #time.sleep(5)
    #emit('event', "false")


@socketio.on('boradcastevent', namespace='/test')
def boradcastevent(json):
    print("Received message: " + json)
    emit('boradcastevent', json, broadcast=True, namespace='/test')

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/api',methods=['GET', 'PUT'])
def api():
    userID = user = request.args.get('userID')
    if (not userID):
        userID = request.form.get('userID')

    deviceID = request.args.get('deviceID')  # if key doesn't exist, returns None
    if (not deviceID):
        deviceID = request.form.get('deviceID')

    deviceState = request.args.get('deviceState')  # if key doesn't exist, returns None
    if (not deviceState):
        deviceState = request.form.get('deviceState')
        if (not deviceState):
            deviceState = "OFF"

    if deviceState == 'ON':
        deviceState = 'true'

    if deviceState == 'OFF':
        deviceState = 'false'

    print(deviceID,deviceState)
    boradcastevent(deviceState)
    #emit('event', deviceState)

    return 'Status changed'





if __name__ == '__main__':
    app.run(debug=True)
    #socketio.run(app,allow_unsafe_werkzeug=True )