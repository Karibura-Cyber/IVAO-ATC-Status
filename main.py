from dataclasses import dataclass
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import discord
import requests, json, os, time
from datetime import date

#Variables unit
config = json.load(open('config.json'))
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
TOKEN = config['token']
URL = "https://api.ivao.aero/v2/tracker/whazzup"
bot = discord.Bot()
page = requests.get(URL)
data = page.json()
now = []
old = []
atc_list = []
pilot_list = []
current_version = 1.2

@bot.event
async def on_ready():
    print(f"[\u001b[32mSUCCESS\u001b[37m] {bot.user.name} is now online. current version is {current_version}") #Prints the bot name and status
    print("[\033[33mINFO\033[0m] Send Message to channel.", config['channel']) #Prints the channel name
    online_check.start()
    print("[\u001b[32mSUCCESS\u001b[37m] Online Check started!")
    version_check.start()
    print("[\u001b[32mSUCCESS\u001b[37m] Version Check started!")

@tasks.loop(seconds=30)
async def online_check():
    page = requests.get(URL) #get data from API
    data = page.json() #convert to json
    with open('now.json', 'w') as f:
            json.dump(data, f) #add to json file

    content = json.load(open('now.json')) #read json file
    for i in data['clients']['atcs']: #find all ATC
        callsign = i['callsign'] #find callsign of ATC
        if config['callsign_prefix'].upper() in callsign[0:2]: #check if the callsign is your ATC
                now.append(callsign) #append callsign to list

    for i in old: #get all callsign from old list
        if i not in now: #if the callsign is not in list now
            print("[\033[91mOFFLINE\033[0m] {} [{}]".format(i, time.strftime("%H:%M:%S"))) 
            embed=discord.Embed()
            embed=discord.Embed(title="{} is now offline".format(i), color=0xff0000)
            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1391075311174000649/8--HPB9-_400x400.jpg")
            msg = await bot.get_channel(int(config['channel'])).send(embed=embed) #Send Offline status when ATC is Offline
            await msg.delete()
            data = atc_list

            for x in data: #if the callsign is in json file
                if x['callsign'] == i:
                    print("[\u001b[32mSUCCESS\u001b[37m] Delete MSG ID: {}".format(x['msg_id']))
                    del_msg = await bot.get_channel(int(config['channel'])).fetch_message(x['msg_id']) #get message id
                    await del_msg.delete() #delete message
                    data.remove(x) #remove the callsign from json file             


    for a in now: #get data from now list                  
        if a not in old:
                #time.sleep(1)
            try:
                atc = data['clients']['atcs']
                for i in atc:     
                    if i['callsign'] == a:
                        frequency = i['atcSession']['frequency']
                        createdAt = i['createdAt']
                        atis = i['atis']
                        lines = atis['lines']
                        vid = i['userId']
                        if len(lines ) > 1:
                                position = lines[1]
                        else:
                                position = "No information"

                        print("[\u001b[32mONLINE\u001b[37m] {} [{}]".format(a, time.strftime("%H:%M:%S")))
                        print("[\u001b[32mSUCCESS\u001b[37m] {} Data loaded!".format(a))
                        embed=discord.Embed()
                        embed=discord.Embed(title="{} is now online".format(a), color=0x00ff00) 
                        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1391075311174000649/8--HPB9-_400x400.jpg")
                        embed.add_field(name="Callsign", value="{}".format(a), inline=False) #Callsign of ATC
                        embed.add_field(name="VID", value="{}".format(vid), inline=False) #Callsign of ATC
                        embed.add_field(name="Position", value="{}".format(position), inline=False)
                        embed.add_field(name="Frequency", value="{}MHz".format(frequency), inline=False) #Freq
                        embed.add_field(name="ATIS", value='\n'.join(map(str, lines)), inline=False) #ATIS of ATC
                        embed.add_field(name="createdAt", value=f"{createdAt}", inline=False)
                        message = await bot.get_channel(int(config['channel'])).send(embed=embed) #Send Embed when ATC is online
                        #append message id to json file
                        atc_list.append({"callsign": a, "msg_id": message.id})
                    
            except:
                pass
        else:
            pass

                     
    for old_atc in content['clients']['atcs']: #find all ATC from previous JSON file
        old_callsign = old_atc['callsign'] #find callsign from old JSON file
        if config['callsign_prefix'].upper() in old_callsign[0:2]: #check if ATC is your country
            old.append(old_callsign) #if ATC is your country then append to list old
    old.clear() #clear all data in list old

    for i in now: #get data from now list
        old.append(i) #append data from now list to old list
    now.clear() #clear all data in now list

    # Check if flights are online
    for pilot in data['clients']['pilots']:
        pilot_callsign = pilot['callsign']
        if pilot_callsign not in pilot_list:
            if pilot_callsign[0:3] in config['flight_callsign_prefix']:
                # Extract necessary information
                user_id = pilot['userId']
                lat = pilot['lastTrack']['latitude']
                lon = pilot['lastTrack']['longitude']
                transponder = pilot['lastTrack']['transponder']
                aircraft_id = pilot['flightPlan']['aircraftId']
                departure_id = pilot['flightPlan']['departureId']
                arrival_id = pilot['flightPlan']['arrivalId']
                
                # Create an embed to display information
                embed = discord.Embed(title=f"Callsign: {pilot_callsign}", color=0x00ff00)
                embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1391075311174000649/8--HPB9-_400x400.jpg")
                embed.add_field(name="UserID", value=user_id, inline=False)
                embed.add_field(name="Lat", value=lat, inline=False)
                embed.add_field(name="Lon", value=lon, inline=False)
                embed.add_field(name="Transponder", value=transponder, inline=False)
                embed.add_field(name="Aircraft ID", value=aircraft_id, inline=False)
                embed.add_field(name="Departure", value=departure_id, inline=False)
                embed.add_field(name="Arrival", value=arrival_id, inline=False)        
                embed.add_field(name="Click to view", value=f"https://webeye.ivao.aero/?pilotId={pilot['id']}", inline=False)
                
                # Send the embed and add the callsign to the list of pilots
                message = await bot.get_channel(int(config['channel'])).send(embed=embed)
                print(f"[ONLINE] {pilot_callsign} [{time.strftime('%H:%M:%S')}]")
                print(f"[SUCCESS] {pilot_callsign} data loaded!")
                pilot_list.append(pilot_callsign)

        else:
            # Check if callsign is still in data, remove it from the list if it's not and send an embed to indicate that it's offline
            if pilot_callsign not in [pilot['callsign'] for pilot in data['clients']['pilots']]:
                pilot_list.remove(pilot_callsign)
                embed = discord.Embed(title=f"Callsign: {pilot_callsign} is offline", color=0x00ff00)
                message = await bot.get_channel(int(config['channel'])).send(embed=embed)



@tasks.loop(seconds=10)
async def version_check():
    r = requests.get("https://raw.githubusercontent.com/Karibura-Cyber/IVAO-ATC-Status/main/version.txt")
    web_version = float(r.text.replace('\n', ''))
    if web_version > current_version:
        print(f"[\033[91mWARNING\033[0m] IVAO ATC Status {web_version} version released! Please update at https://github.com/Karibura-Cyber/IVAO-ATC-Status") 
        await bot.get_channel(int(config['channel'])).send(f"IVAO ATC Status {web_version} version released! Please update")
        version_check.stop()

#Command sections
@bot.command()
async def track(ctx, flight_number: str):     
     for i in data['clients']['pilots']:
        if i['callsign'] == flight_number.upper():
            #make embed show callsign, userid, lastTrack latitude and longitude, transponder, flightPlan aircraftId departureId and arrivalId
            userID = i['userId']
            lat = i['lastTrack']['latitude']
            lon = i['lastTrack']['longitude']
            transponder = i['lastTrack']['transponder']
            aircraft_id = i['flightPlan']['aircraftId']
            departure_id = i['flightPlan']['departureId']
            arrival_id = i['flightPlan']['arrivalId']

            embed=discord.Embed()
            embed=discord.Embed(title="Callsign: {}".format(flight_number), color=0x00ff00)
            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1391075311174000649/8--HPB9-_400x400.jpg")
            embed.add_field(name="UserID", value="{}".format(userID), inline=False)
            embed.add_field(name="Lat", value="{}".format(lat), inline=False)
            embed.add_field(name="Lon", value="{}".format(lon), inline=False)
            embed.add_field(name="Transponder", value="{}".format(transponder), inline=False)
            embed.add_field(name="Aircraft ID", value="{}".format(aircraft_id), inline=False)
            embed.add_field(name="Departure", value="{}".format(departure_id), inline=False)
            embed.add_field(name="Arrival", value="{}".format(arrival_id), inline=False)        
            embed.add_field(name="Click to view", value="https://webeye.ivao.aero/?pilotId={}".format(i['id']), inline=False)
            message = await ctx.send(embed=embed)

bot.run(TOKEN)