import os
import sys
import math
import json
import aiohttp
import random
import discord
import asyncio
import datetime
import random
from time import ctime

client = discord.Client()
NetmessageVar = 0
channel = discord.Object(id='414463625546301473') #'402095445901312000  | '399446862442266636 
network = discord.Embed()
counter = 0
headers = {'content-type': 'text/html'}
async def my_background_task():
    global NetmessageVar
    global counter
    await client.wait_until_ready()
    while not client.is_closed:
        date = datetime.datetime.now()
        if counter >= 5:
            counter = 0
            print("\n\nCreating a new message to avoid timeout\n\n")
            await client.delete_message(NetmessageVar)
            NetmessageVar = await client.send_message(channel, embed=network)
        if NetmessageVar != 0:
            async with aiohttp.get(url=await GetExplorer() + 'api/getnetworkhashps', headers=headers) as aiokhs:
                khs = convert_size(float(await aiokhs.text()))
            # NETWORK
            network = discord.Embed(color=0x80ff80)
            network.set_author(name="Garlicoin",icon_url="http://garlicoin.io/static/logo.040b5384.png")
            network.add_field(name="Network Hashrate", value=khs, inline=True)
            network.add_field(name="Price", value="$" +
                              await getPrice() + "USD", inline=True)
            #network.add_field(name="Last Updated", value=ctime(), inline=False)
            network.add_field(name="\u200b", value="\u200b", inline=False)
            try:
                poolInfo = await getPoolInfo()
            except:
                poolInfo = {"Error": "Unable to connect to watchdog!"}
            keys = list(poolInfo.keys())
            random.shuffle(keys)
            for key in keys:
                network.add_field(name=key, value=poolInfo[key], inline=True)
            network.add_field(name="\u200b", value="\u200b", inline=False)
            network.add_field(name='Support The Bot', value='GUdBoyeDgTqapnN15L3QkQBjnmp7E8FhqT', inline=False)
            await client.edit_message(NetmessageVar, embed=network)
            print("Updated Message\nWaiting 30 seconds")
            await asyncio.sleep(30.0)
            counter+=1
    print("\n\nCLIENT CONNECTION CLOSED!!!\n\n")


async def getPoolInfo():
    print("Grabbing pool info!")
    returnDict = {}
    try:
        async with aiohttp.get(url="https://watchdog.garli.co.in/api/v1/stats") as v:
            v = json.loads(await v.text())
            keys = v['data'].keys()
            for key in keys:
                stats = v['data'][key]['stats'].keys()
                try:
                    returnDict[v['data'][key]['pool']['name']] = convert_size(v['data'][key]['stats'][max(stats)]['hashrate'])
                except:
                    returnDict[v['data'][key]['pool']['name']] = convert_size(0)
    except Exception as e:
        returnDict["Error"] = "Json Decode Error: Unable to connect to watchdog (502)"
    return returnDict

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0H/s"
    size_name = ("H/s", "KH/s", "MH/s", "GH/s", "TH/s",
                 "PH/s", "EH/s", "ZH/s", "YH/s")
    i = int(math.floor(math.log(size_bytes, 1000)))
    s = round(size_bytes / math.pow(1000, i), 2)
    return "%s %s" % (s, size_name[i])


async def getPrice():
    while True:
        try:
            async with aiohttp.get(url='http://api.coinmarketcap.com/v1/ticker/garlicoin/', headers=headers) as priceJSON:
                priceJSON = json.loads(await priceJSON.text())
            priceJSON = priceJSON[0]
            return str(round(float(priceJSON['price_usd']), 3))
        except:
            print("Cannot connect to Coin Market Cap trying again in 5 seconds")
            time.sleep(5)


async def GetExplorer():
    explorers = [
        "http://garli.co.in/",
                "http://explorer.garlicoin.com"
    ]
    i = 0
    oSwitch = 0
    while i <= len(explorers):
        try:
            async with aiohttp.get(explorers[i]+"api/getnetworkhashps", headers=headers) as test:
                test = json.loads(await test.text())
            print("Connected to explorer " + explorers[i] + " ")
            explorerURL = explorers[i]
            return explorerURL
        except:
            print("Cannot connect to prefered explorer trying next address")
            i += 1
    print("Failed to connect to any explorers trying again in 5 seconds")
    time.sleep(5)
    GetExplorer()


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Clearing Channel')
    await client.purge_from(channel, limit=1)
    global NetmessageVar
    print("Sending setup message")
    NetmessageVar = await client.send_message(channel, embed=network)
    client.loop.create_task(my_background_task())
try:
    with open('key.txt', 'r') as keyFile:
        keySecret = keyFile.read()
    client.run(keySecret)
except Exception as E:
    print("Haha yes Aussie internet ftw\n")
    print(" ,-_|\\")
    print("/     \\ STRAYA")
    print("\_,-._/")
    print("     v")
    print("\nActual tho cant connect to discord servers,\n")
    print(E)
    exit()
print("Something didnt run")
#except Exception as E:
#;    print("OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this!")
#    print(E)
#    os.system('python3 bot.py')
