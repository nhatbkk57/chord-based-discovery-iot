# chord-based-discovery-iot


## progress

- Implemented Chord basic operatior (join, leave, lookup ...) on 1 ring
- Implemented hashing sha1 for key 

## install
- install Flask web service: sudo pip install Flask 
- Clone or Download git repository: https://github.com/nhatbkk57/chord-based-discovery-iot.git
## usage

### step 1: run Flask web service
python app.py

### step 2: send URL request to generate environment
Example:
curl --data "numring=1&numnode=100&numsensor=300" http://127.0.0.1:5000/env

### send URL request to lookup keyID at nodeID
Example:
curl --data "nodeID=791&keyID=1410836122761576493812106956022308740271657004473" http://127.0.0.1:5000/lookup

### send URL request to print environment in json format
curl http://127.0.0.1:5000/print