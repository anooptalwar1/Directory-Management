#!/usr/bin/env python3


from threading import Thread
import os, sys
from handledir import dirmanage, undodir
import functools
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
from flask import Flask, flash, request, redirect, Response, render_template, abort, jsonify, send_from_directory, send_file, abort
from flask_socketio import SocketIO, ConnectionRefusedError

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

clients = []

@socketio.on('connect')
def test_connect(json, methods=['POST']):
    print('received event: ' + str(json))
    content = json
    userid = content['userid']
    if userid in clients:
        socketio.send('Clients already connected')
        # TO DO Reject socket connection
    else:
        clients.append[userid]
        dirmanage.create_user_dir(userid)
        socketio.emit('connected', json, callback=messageReceived)

@socketio.on('disconnect')
def test_disconnect(json, methods=['POST']):
    content = json
    userid = content['userid']
    clients.pop[userid]
    # TODO user disconnection
    print('Client disconnected')

""" Create directory based on userid  """
@app.route('/app/create', methods=['POST'])
def create_userdir():
    if request.method == 'POST':
        content = request.json
        userid = content['userid']
        dirmanage.create_user_dir(userid)
        return jsonify(userid + " Directory Created")

""" Create directory based on userid and project """
@app.route('/app/create/project', methods=['POST'])
def create_projectdir():
    if request.method == 'POST':
        content = request.json
        userid = content['userid']
        project = content['project']
        dirmanage.create_user_dir(userid, project)
        return jsonify(project + " Directory Created for " + userid)

""" Create Custom directory based on userid and project """
@app.route('/app/create/customdir', methods=['POST'])
def create_customdir():
    if request.method == 'POST':
        content = request.json
        userid = content['userid']
        project = content['project']
        user_input = content['custom']
        PROJECT_DIRECTORY = "users" + "/" + userid + "/" + project + "/"
        dirmanage.create_user_dir(userid, project, user_input)
        return jsonify(user_input + " Directory Created for " + PROJECT_DIRECTORY)
        
""" List All directory based on userid """
@app.route('/app/list/customdir', methods=['GET'])
def list_dir():
    if request.method == 'GET':
        content = request.json
        userid = content['userid']
        return Response(dirmanage.list_custom_dir(userid))

""" Delete directory tree based on userid """
@app.route('/app/delete/user', methods=['DELETE'])
def delete_user_dir():
    if request.method == 'DELETE':
        content = request.json
        userid = content['userid']
        return Response(dirmanage.delete_user_dir(userid))

""" Delete directory based on userid and project """
@app.route('/app/delete/projectdir', methods=['DELETE'])
def delete_project_dir():
    if request.method == 'DELETE':
        content = request.json
        userid = content['userid']
        project = content['project']
        return Response(dirmanage.delete_user_project_dir(userid, project))

""" Delete directory based on userid and project """
@app.route('/app/delete/customdir', methods=['DELETE'])
def delete_custom_dir():
    if request.method == 'DELETE':
        content = request.json
        userid = content['userid']
        project = content['project']
        customdir = content['custom']
        return Response(dirmanage.delete_custom_dir(userid, project, customdir))

""" Rename directory based on userid and project """
@app.route('/app/rename/customdir', methods=['PUT'])
def rename_customdir():
    if request.method == 'PUT':
        content = request.json
        userid = content['userid']
        project = content['project']
        customdir = content['custom']
        new_user_input = content['newcustomname']
        return Response(dirmanage.rename_custom_dir(userid, project, customdir, new_user_input))

""" Undo directory based on userid and project """
@app.route('/app/undo/customdir', methods=['POST'])
def undo_customdir():
    if request.method == 'POST':
        content = request.json
        userid = content['userid']
        return Response(undodir.undo_dir(userid))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6543, debug=True)
