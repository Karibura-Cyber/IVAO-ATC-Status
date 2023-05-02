<!--# 🛑BOT NOT WORK NOW!! I'LL FIX IT ASAP.🛑
<hr>-->
### Current version : 1.2

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
    "callsign_prefix": "<Airport ICAO Code Prefix EX: VT for Thailand Airport>",
    "flight_callsign_prefix": "<Flight Number prefix  only one airline EX: DHL>"
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
- 2022/10/12 Version checking system
- 2022/10/16 VID
- 2023/5/2   Airline Tracking auto & /track command

### Command
```
/track <Flight Number>
```


### License
MIT License

# If You have question or problem of this bot please contact me.
Email: meck22772@gmail.com
Discord: Meck#1155
