from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sid123'
socketio = SocketIO(app)
    
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1,username='Sid', password='test'))
users.append(User(id=2,username='NotSid', password='sec'))    
    
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
    
    
    
    

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.password == password][0]
        if user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('sessions'))

        return redirect(url_for('sessions'))

    return render_template('login.html')

@app.route('/')
def sessions():
    return render_template('index.html')
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
app.run(debug=True)