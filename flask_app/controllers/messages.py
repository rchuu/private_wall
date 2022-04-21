from flask import render_template, session, flash, redirect, request
import re
from flask_app import app
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/post_message', methods=["POST"])
def post_message():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "sender_id": request.form['sender_id'],
        "receiver_id": request.form['receiver_id'],
        "content": request.form['content']
    }
    Message.save(data)
    return redirect('/success')


@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/success')
