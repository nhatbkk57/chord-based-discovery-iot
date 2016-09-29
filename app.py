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
        return json.dumps("OK",indent=4, sort_keys=True)
    else:
        return json.dumps("Failed",indent=4, sort_keys=True)

@app.route('/lookup', methods=['POST'])
def lookup():
    if request.method == 'POST':
        nodeID = int(request.form['nodeID'])
        keyID = int(request.form['keyID'])
        return main.lookup(nodeID,keyID)

@app.route('/join', methods=['POST'])
def join():
    if request.method == 'POST':
        nodeID = int(request.form['nodeID'])
        nodeOld = int(request.form['nodeOld'])
    if (main.join(nodeID,nodeOld)):
        return json.dumps("OK")
    else:
        return json.dumps("Failed")

@app.route('/print', methods=['GET'])
def print_():
    json_ = main.print_()
    return json_

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        nodeID = int(request.form['nodeID'])
        sensorID = int(request.form['sensorID'])
        return json.dumps(main.insert(nodeID,sensorID))

@app.route('/test1', methods=['GET'])
def test1():
    return json.dumps(main.test1(),indent=4, sort_keys=True)

@app.route('/test2', methods=['GET'])
def test2():
    return json.dumps(main.test2(),indent=4, sort_keys=True)

@app.route('/test3', methods=['GET'])
def test3():
    return json.dumps(main.test3(),indent=4, sort_keys=True)

# @app.route('/testlookup', methods=['GET'])
# def testLookup():
#     return main.testlookup()


if __name__ == '__main__':
    app.run()
