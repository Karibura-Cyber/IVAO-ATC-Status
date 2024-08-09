Discord Bot for check ATC is online or offline and send data to your Discord server

### Setup
MAKE A SUB DOMIAN <br>
1.Go To File Sub Domain and upload it and extract it
go to discord Developer and make a bot

 go to SSH and type
```bash
  pip install -r requirements.txt
```
### Config
Go to <code>config.json</code> and fill your data
```bash
{
    "token": "<Bot Token>",
    "channel": "<Channel ID>",
    "airport_prefixes": ["OJAI", "OSDI",] #CHANGE DESIRE AIRPORT ONLY PUT THE ICAO OF THE AIRPORT
}

bot must have : bot ,view channels ,  send messages ,  embed links ,  read message history

 After editing Code go SSH and CD atc.yourdivison.ivao.aero
 then run 
```
test code 

Linux
```bash
  python3 main.py
```
if everything works use this code to keep the bot online
```bash
  screen -dmS bot-name python3.9 main.py
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


<hr>

Special thanks <br>
https://github.com/enimri - 633950 lyad
