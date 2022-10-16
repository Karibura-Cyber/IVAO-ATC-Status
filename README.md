# IVAO-ATC-Status
Discord Bot for check ATC is online or offline and send data to your Discord server

You can push it to Heroku for 24/7 runtime

### Setup
```bash
  pip install -r requirements.txt
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

### Bot Commands
METAR
```bash
  /metar
```
TAF
```bash
  /taf
```
HELP
```bash
  /help
```

### ChangeLog
- 2022/10/12 METAR & TAF command
- 2022/10/12 Version checking system
- 2022/10/16 VID

### License
MIT License
