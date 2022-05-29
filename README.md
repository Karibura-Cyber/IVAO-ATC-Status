# IVAO-ATC-Status
Discord Bot for check ATC is online or offline and send data to your Discord server

All data is from IVAO Whazzup Public API

!! WARNING !! Don't Delete <code>atc.json</code>

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
    "prefix": "<Bot Prefix>",
    "callsign_prefix": "<Airport ICAO Code Prefix EX: VT for Thailand Airport>"
}
```

### Run program
```bash
  python main.py
```


### License
MIT License
