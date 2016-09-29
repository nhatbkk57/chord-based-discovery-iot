curl --data "numring=3&numnode=20&numsensor=50" http://127.0.0.1:5000/env | python -m json.tool
curl http://127.0.0.1:5000/test3 | python -m json.tool