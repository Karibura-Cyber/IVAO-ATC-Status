from dataclasses import dataclass
from discord.ext import commands
from discord.ext.commands import Bot
import discord
import requests, json, os, time

#Variables unit
config = json.load(open('config.json'))
TOKEN = config['token']
URL = "https://api.ivao.aero/v2/tracker/whazzup"
bot = commands.Bot(command_prefix='!!')
page = requests.get(URL)
data = page.json()
now = []
old = []
atc_list = []

@bot.event
async def on_ready():
    print("[\033[33mINFO\033[0m] Bot is ready.", bot.user.name) #Prints the bot name and status
    print("[\033[33mINFO\033[0m] Send Message to channel.", config['channel']) #Prints the channel name
    while True:
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
                #await msg.delete(delay=3)
                data = atc_list #json.load(open('atc.json')) #read json file

                for x in data: #if the callsign is in json file
                    if x['callsign'] == i:
                        print("[\u001b[32mSUCCESS\u001b[37m] Delete MSG ID: {}".format(x['msg_id']))
                        del_msg = await bot.get_channel(int(config['channel'])).fetch_message(x['msg_id']) #get message id
                        await del_msg.delete() #delete message
                        data.remove(x) #remove the callsign from json file
                        with open('atc.json', 'w') as f:
                            json.dump(data, f)              


        for a in now: #get data from now list                  
            if a not in old:
                time.sleep(1)
                atc = data['clients']['atcs']
                for i in atc:     
                    if i['callsign'] == a:
                        frequency = i['atcSession']['frequency']
                        createdAt = i['createdAt']
                        atis = i['atis']
                        lines = atis['lines']

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
                        # embed.add_field(name="Server ID", value="{}".format(serverID), inline=False) #Server ID
                        # embed.add_field(name="Voice", value="{}".format(lines[0]), inline=False) #Voice Server
                        embed.add_field(name="Position", value="{}".format(position), inline=False)
                        embed.add_field(name="Frequency", value="{}MHz".format(frequency), inline=False) #Freq
                        embed.add_field(name="ATIS", value='\n'.join(map(str, lines)), inline=False) #ATIS of ATC
                        embed.add_field(name="createdAt", value=f"{createdAt}", inline=False)
                        message = await bot.get_channel(int(config['channel'])).send(embed=embed) #Send Embed when ATC is online
                        #append message id to json file
                        atc_list.append({"callsign": a, "msg_id": message.id})
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
        time.sleep(30)
bot.run(TOKEN)
