from flask import Flask, render_template
from flask_socketio import SocketIO,emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('event')
def event(json):
    print("Received message: " + json)
    emit('event', json)
    #time.sleep(3)
    #emit('event', "true")
    #time.sleep(5)
    #emit('event', "false")




@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass


@app.route("/")
def hello_world():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)