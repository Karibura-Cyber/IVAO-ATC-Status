<!--# 🛑BOT NOT WORK NOW!! I'LL FIX IT ASAP.🛑
<hr>-->
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
    "callsign_prefix": "<Airport ICAO Code Prefix EX: VT for Thailand Airport | Prefix is mean start with that string>"
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
- 2022/10/16 VID
- 2023/8/2 Refactor code

### Command
```
/metar <ICAO>
/taf <ICAO>
```


### License
MIT License

# If You have question or problem of this bot please contact me.
Email: meck22772@gmail.com<br>
Discord: Meck#1155<br>
Nostr: npub1tx9djndf23ld0fkfw0zl4zn77f4rhqxy0a3kh8vj6dtv4edjgdeq6d95lq
