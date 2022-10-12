# IVAO-ATC-Status
Discord Bot for check ATC is online or offline and send data to your Discord server

All data is from IVAO Whazzup Public API

### Setup
```bash
  pip install -r requirement.txt
```
### Config 
Go to <code>config.json</code> and fill your data
```bash
{
    "token": "<Bot Token>",
    "channel": "<Channel ID>",
    "callsign_prefix": "<Airport ICAO Code Prefix EX: VT for Thailand Airport>"
}
```

### Run program
Windows
```bash
  python main.py
```

Linux
```bash
  python3 main.py
```

### ChangeLog
- 2022/10/12 METAR & TAF command

### License
MIT License
