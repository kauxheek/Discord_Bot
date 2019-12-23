import discord
from pyowm import OWM
import urllib.request
import urllib.parse
import re
import wikipedia

client = discord.Client() #a client connection that connects to Discord


@client.event
async def on_message(message):
    pbh_guild = client.get_guild('your guild id')  # your guild id
    if message.author == client.user:
        return
    if "member_count" == message.content.lower():
        await message.channel.send(pbh_guild.member_count)

    # getting youtube links
    x = message.content  # get the content from the user
    if message.content.startswith("$song"):  # if the content starts with '$song' e.g $song numb
        query_string = urllib.parse.urlencode({"search_query": x})  # returns the key value pairs
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string)  # browses to the url and return a url object
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})',
                                    html_content.read().decode())  # href=”/watch?v=<11_DIGIT_IDENTIFIER>
        # getting 11 digit identfier using regular expression

        x = ("http://www.youtube.com/watch?v=" + search_results[1])  # getting the 2nd result
        await message.channel.send(x)  # sending out the result

    # for extracting info from wikipedia
    y = message.content  # getting the  from the users
    if message.content.startswith("?"):  # if the content starts with '?' e.g. ?india
        try:  # then execute this block
            y = wikipedia.summary(y,sentences=4)  # getting the wiki summary of the content(e.g. ?india) upto 4 sentences
            await message.channel.send(y)  # sending the wiki info
        except:
            await message.channel.send("Not found!!try with another keyword")  # if the content not found in wikipedia

    if "member_status" == message.content.lower():  # getting current member info
        online = 0
        offline = 0
        idle = 0
        member_online = pbh_guild.members #getting the members
        for m in member_online:  #checkijng for each member
            if str(discord.Status == "online"): #if Status is online increment online by 1
                online = online + 1
            elif str(discord.Status == "offline"):
                offline += 1
            else:
                idle += 1
        await message.channel.send(f"Online: {online}.\nOffline: {offline}.\nIdle: {idle}")
    if message.content.startswith("$hello"):
        await message.channel.send("hello! " + message.author.name)
    if message.content.startswith("$PBH"):
        await message.channel.send("peace before heaven")
    if message.content.startswith("$cmd_list"):
        await message.channel.send(
            "1.$PBH\t2.member_status\t3.member_count\n4.any place name for weather report\n5.$song song_name\t6.? text for wiki")
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    # getting weather report
    API_key = 'api_key_of_pyowm'  # your api key for pyowm
    owm = OWM(API_key)
    try:
        place = message.content.lower()
        weather = owm.weather_at_place(place)
        w = weather.get_weather() #getting the weather from weather_at_place
        humidity = w.get_humidity() #getting humidity
        pressure = w.get_pressure() #getting pressure
        w = w.get_temperature('celsius') #getting temperature
        await message.channel.send(f"Temperature:{w}\nHumidity: {humidity}\nPressure: {pressure}")

    except:
        return #just return if the content not found


client.run('discord_client_id')  # your client id
