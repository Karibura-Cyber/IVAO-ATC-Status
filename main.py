import discord, csv, requests, json, datetime, os
from discord.ext import tasks
from functions import *

bot = discord.Bot()

now_data = []
pre_data = []

with open('config.json', 'r') as raw:
    config = json.load(raw)

@bot.event
async def on_ready():
    log.success(f"{bot.user} is ready and online!")
    send_status.start()

@bot.command(description="Sends the bot's latency.") 
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")
    log.success(f"Pong! Latency: {bot.latency}")

@bot.command(description="Use for get IVAOTH Members Data")
async def members(ctx):
    file_path = 'IVAOTH_Members.csv'
    names_list = []
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            names_list.append(row['Name'])

    names_text = '\n'.join(names_list)

    with open('IVAOTH_Members.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(names_text)

    with open('IVAOTH_Members.txt', 'rb') as file:
        await ctx.send(file=discord.File(file, 'IVAOTH_Members.txt'))
        log.success("IVAOTH Members list sent")

    os.remove('IVAOTH_Members.txt')
    log.success("IVAOTH_Members.txt has deleted")

@bot.command(description="Request Airport METAR")
async def metar(ctx, icao:str):
    url = f"https://api.met.no/weatherapi/tafmetar/1.0/metar.txt?icao={icao.upper()}"
    data = requests.get(url).text.split('\n')
    index = len(data)-3
    await ctx.respond(data[index])

@bot.command(description="Request Airport TAF")
async def taf(ctx, icao:str):
    url = f"https://api.met.no/weatherapi/tafmetar/1.0/taf.txt?icao={icao.upper()}"
    data = requests.get(url).text.split('\n')
    index = len(data)-3
    await ctx.respond(data[index])

@tasks.loop(seconds=30)
async def send_status():
    global now_data, pre_data
    channel = bot.get_channel(int(config['channel_id']))

    if channel is not None:
        try:
            url = 'https://api.ivao.aero/v2/tracker/whazzup'
            r = requests.get(url)
            data = r.json()
            callsigns = [i['callsign'] for i in data['clients']['atcs'] if i['callsign'].startswith(config['airport_prefix'])]
            now_data = callsigns

            # Check for offline callsigns
            for callsign in pre_data:
                if callsign not in now_data:
                    id = message.get_id()
                    msg = await channel.fetch_message(id[callsign])
                    await msg.delete()
                    await channel.send(f"{callsign} is now offline", delete_after=5)                    
                    log.warning(f"{callsign} is now offline")

            # Check for online callsigns
            for callsign in now_data:
                if callsign not in pre_data:
                    atc_data = next((i for i in data['clients']['atcs'] if i['callsign'] == callsign), None)
                    if atc_data:
                        timestamp = datetime.datetime.utcnow()
                        atis_data = atc_data.get('atis', {})
                        atis_lines = atis_data.get('lines', [])
                        position = atis_lines[1] if len(atis_lines) > 1 else "N/A"
                        user_id = atc_data.get('userId', 'N/A')
                        embed = discord.Embed(title=f"{callsign} is now online", url=f"https://webeye.ivao.aero/?atcId={atc_data['id']}", color=0x00ff00)
                        embed.add_field(name="VID", value=user_id, inline=True)
                        embed.add_field(name="Position", value=position, inline=True)
                        embed.add_field(name="Frequency", value=atc_data.get('atcSession', {}).get('frequency', 'N/A'), inline=True)
                        embed.add_field(name="ATIS", value="\n".join(atis_lines), inline=False)
                        embed.add_field(name="TimeStamp", value=timestamp, inline=False)
                        msg = await channel.send(embed=embed)
                        message.add_id(callsign, msg.id)
                        log.success(f"{callsign} is now online")
                        #log.success(message.get_id()[callsign])
                    else:
                        log.error(f"{callsign} data not found")

            # Update the previous data
            pre_data = now_data
        except requests.RequestException:
            await channel.send("Failed to fetch data from IVAO API.")
            log.error("Failed to fetch data from IVAO API.")
    else:
        log.error(f"{channel} channel not found")


bot.run(config['token'])