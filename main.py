import discord
import csv
import requests
import json
import datetime
import os
import logging
from discord.ext import tasks

# Setup logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('discord')

bot = discord.Bot()

now_data = {}
pre_data = {}
message_ids = {}  # Dictionary to track message IDs

with open('config.json', 'r') as raw:
    config = json.load(raw)

@bot.event
async def on_ready():
    log.info(f"{bot.user} is ready and online!")
    send_status.start()

@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency:.2f} seconds")
    log.info(f"Pong! Latency: {bot.latency:.2f}")

@bot.command(description="Use to get IVAO Members Data")
async def members(ctx):
    file_path = 'IVAO_Members.csv'
    names_list = []

    try:
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                names_list.append(row['Name'])

        names_text = '\n'.join(names_list)

        with open('IVAO_Members.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(names_text)

        with open('IVAO_Members.txt', 'rb') as file:
            await ctx.send(file=discord.File(file, 'IVAO_Members.txt'))
            log.info("IVAO Members list sent")

        os.remove('IVAO_Members.txt')
        log.info("IVAO_Members.txt has been deleted")

    except Exception as e:
        await ctx.send("An error occurred while processing the IVAO Members data.")
        log.error(f"Error in members command: {e}")

@bot.command(description="Request Airport METAR")
async def metar(ctx, icao: str):
    url = f"https://api.met.no/weatherapi/tafmetar/1.0/metar.txt?icao={icao.upper()}"
    try:
        data = requests.get(url).text.split('\n')
        index = len(data) - 3
        await ctx.respond(data[index])
    except requests.RequestException as e:
        await ctx.respond("Failed to fetch METAR data.")
        log.error(f"Error fetching METAR data: {e}")

@bot.command(description="Request Airport TAF")
async def taf(ctx, icao: str):
    url = f"https://api.met.no/weatherapi/tafmetar/1.0/taf.txt?icao={icao.upper()}"
    try:
        data = requests.get(url).text.split('\n')
        index = len(data) - 3
        await ctx.respond(data[index])
    except requests.RequestException as e:
        await ctx.respond("Failed to fetch TAF data.")
        log.error(f"Error fetching TAF data: {e}")

@tasks.loop(seconds=30)
async def send_status():
    global now_data, pre_data
    channel = bot.get_channel(int(config['channel_id']))

    if channel is not None:
        try:
            url = 'https://api.ivao.aero/v2/tracker/whazzup'
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            # Collect callsigns for all configured airport prefixes
            now_data = {}
            for prefix in config['airport_prefixes']:
                callsigns = [i['callsign'] for i in data['clients']['atcs'] if i['callsign'].startswith(prefix)]
                now_data.update({prefix: callsigns})

            # Check for offline callsigns
            for prefix, callsigns in pre_data.items():
                for callsign in callsigns:
                    if callsign not in now_data.get(prefix, []):
                        if callsign in message_ids:
                            msg_id = message_ids.pop(callsign)
                            try:
                                msg = await channel.fetch_message(msg_id)
                                await msg.delete()
                            except discord.NotFound:
                                log.warning(f"Message with ID {msg_id} not found")
                            await channel.send(f"{callsign} is now offline", delete_after=5)
                            log.info(f"{callsign} is now offline")

            # Check for online callsigns
            for prefix, callsigns in now_data.items():
                for callsign in callsigns:
                    if callsign not in pre_data.get(prefix, []):
                        atc_data = next((i for i in data['clients']['atcs'] if i['callsign'] == callsign), None)
                        if atc_data:
                            timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                            atis_data = atc_data.get('atis', {})
                            atis_lines = atis_data.get('lines', [])
                            position = atis_lines[1] if len(atis_lines) > 1 else "N/A"
                            user_id = atc_data.get('userId', 'N/A')
                            embed = discord.Embed(
                                title=f"{callsign} is now online",
                                url=f"https://webeye.ivao.aero/?atcId={atc_data['id']}",
                                color=0x00ff00
                            )
                            embed.add_field(name="VID", value=user_id, inline=True)
                            embed.add_field(name="Position", value=position, inline=True)
                            embed.add_field(name="Frequency", value=atc_data.get('atcSession', {}).get('frequency', 'N/A'), inline=True)
                            embed.add_field(name="ATIS", value="\n".join(atis_lines), inline=False)
                            embed.add_field(name="TimeStamp", value=timestamp, inline=False)
                            msg = await channel.send(embed=embed)
                            message_ids[callsign] = msg.id
                            log.info(f"{callsign} is now online")
                        else:
                            log.error(f"{callsign} data not found")

            # Update the previous data
            pre_data = now_data
        except requests.RequestException as e:
            await channel.send("Failed to fetch data from IVAO API.")
            log.error(f"Failed to fetch data from IVAO API: {e}")
        except discord.DiscordException as e:
            await channel.send("An error occurred while interacting with Discord.")
            log.error(f"Discord error: {e}")
        except Exception as e:
            await channel.send("An unexpected error occurred.")
            log.error(f"An unexpected error occurred: {e}")
    else:
        log.error(f"Channel with ID {config['channel_id']} not found")

bot.run(config['token'])
