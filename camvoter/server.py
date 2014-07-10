from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from random import randint
import logging
logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
import random
import SimpleCV as scv
import cvutils
from camvoter import CamVoterHSV, CamVoterCol

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#display = scv.Display()
cam = scv.Camera()
camv = CamVoterHSV()
imageCount = 1
maxImages = 100

@app.route('/')
def index():
    return render_template('fx.html')

@socketio.on('get votes', namespace='/test')
def test_message(message):
    global imageCount
    camv.set_image(cam.getImage().flipHorizontal())
    votes = camv.get_vote_count()
    logger.debug('We have %d votes'%votes)
    #votes = random.randrange(1,2)
    if False:
        camv.image_hot.save('images/cam{}.jpg'.format(imageCount))
        imageCount+=1
        if imageCount == maxImages :
            imageCount = 0;

    #print( 'target {}'.format( camv.area_max ) );
    #for b in camv.all_blobs:
    #    print('blob {}, {}'.format(b.angle(),b.area()))
    emit('vote count', {'data': {'count': votes}})
    
    #if votes:
    #    for b in camv.filtered_blobs:
    #        camv.image.drawCircle((b.x, b.y), 5, scv.Color.RED)
    #camv.image.show()

@socketio.on('set params', namespace='/test')
def set_params(message):
    camv.__dict__.update(message)
    

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app)
