from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm
import Crypto.PublicKey.RSA as RSA


@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        new_key = RSA.generate(1024,e=65537)
        public = new_key.publickey().exportKey('PEM').decode('ascii')
        private = new_key.exportKey('PEM').decode('ascii')
        session['public_key']=public
        session['private_key']=private
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.email.data = session.get('email', '')
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    private_key=session.get('private_key','')
    public_key=session.get('public_key','')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html',public_key=public_key, private_key=private_key, name=name, room=room)
