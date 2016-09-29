curl --data "numring=2&numnode=10&numsensor=20" http://127.0.0.1:5000/env | python -m json.tool
curl http://127.0.0.1:5000/test1 | python -m json.tool