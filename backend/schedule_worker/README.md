Welcome to schedule worker!
===================

To install:
```
[schedule_worker] python3 -m virtualenv MojEnv
[schedule_worker] . ./MojEnv/bin/activate
(MojEnv) [schedule_worker] pip install -r requirements.txt
Collecting coloredlogs==5.2 (from -r requirements.txt (line 1))
...
```

To run:
```
python3 main.py PORT_NUMBER
python3 main.py 8888
```

To send request:
```
curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://0.0.0.0:8888/healthcheck
{"number": 4, "status": "OK"}%
```

Enjoy ;)
