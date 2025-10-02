### Python system snapshot utility package
This python app monitors your system/server. Output is written to a json file and stdout.

It creates snapshots of the state of the system each 30 seconds (configurable):

    {"Tasks": {"total": 440, "running": 1, "sleeping": 354, "stopped": 1, "zombie": 0},
    "%CPU": {"user": 14.4, "system": 2.2, "idle": 82.7},
    "KiB Mem": {"total": 16280636, "free": 335140, "used": 11621308},
    "KiB Swap": {"total": 16280636, "free": 335140, "used": 11621308},
    "Timestamp": 1624400255}

Tool name is **snapshot**
The package has the following structure:
```bash
Python_snapshot_util
├── snapshot
│   ├── __init__.py
│   ├── snapshot.py
│   ├── snapshot.json
│   └── README.md
├── requirements.txt
├── tox.ini
├── README.md
└── setup.py
```

Verify package:

    cd ..
    snapshot-util$ pip install -U ./snapshot-util
    snapshot-util$ snapshot -i 1
