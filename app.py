#!flask/bin/python
#!pandas/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import main
import json
app = Flask(__name__)

@app.route('/env', methods=['POST'])
def gen_evn():
    if request.method == 'POST':
        numring = int(request.form['numring'])
        numnode = int(request.form['numnode'])
        numsensor = int(request.form['numsensor'])
    if (main.gen_env(numring,numnode,numsensor)):
        return json.dumps("OK")
    else:
        return json.dumps("Failed")

@app.route('/lookup', methods=['POST'])
def lookup():
    if request.method == 'POST':
        nodeID = int(request.form['nodeID'])
        keyID = int(request.form['keyID'])
    return main.lookup(nodeID,keyID)

@app.route('/print', methods=['GET'])
def print_():
    json_ = main.print_()
    return json_

if __name__ == '__main__':
    app.run()
