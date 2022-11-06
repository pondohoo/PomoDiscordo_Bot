# This example requires the 'message_content' intent.
import discord
from discord.ext import commands
import os
import asyncio
import time

status = 0
seconds = 0

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!pom ', intents=intents)

def minutesToSeconds(minute):
  return minute * 60

def secondsToTime(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
  
    return "%d:%02d:%02d" % (hour, minutes, seconds)
  

async def pomodoro(pomodorotime, breaktime, intervals, ctx):
  for n in range(intervals):
    if status == 0:
      return
    currentPomodoroTime = minutesToSeconds(pomodorotime)
    notification = currentPomodoroTime / 4 
    timestring = secondsToTime(currentPomodoroTime)
    await ctx.send("```STARTING POMODORO %d```" %(n+1))
    await asyncio.sleep(1)
    await ctx.send("```TIME REMAINING:  %s```" %timestring)
    currentPomodoroTime -= notification
    while currentPomodoroTime > 0:
      if status == 0:
        return
          
      timestring = secondsToTime(currentPomodoroTime)
      await asyncio.sleep(notification)
      await ctx.send("```TIMELEFT:  %s```" %timestring)
      currentPomodoroTime -= notification
      
    
    await asyncio.sleep(notification)
    await ctx.send("```DONE```")
    await asyncio.sleep(1)
    await ctx.send("```STARTING BREAK```")
    await asyncio.sleep(1)
    
    currentBreakTime = minutesToSeconds(breaktime)
    breakNotification = currentBreakTime / 4
    breaktimestring = secondsToTime(currentBreakTime)
    await ctx.send("```TIME REMAINING:  %s```" %breaktimestring)
    currentBreakTime -= breakNotification
    
    while currentBreakTime > 0:
      if status == 0:
        return
      breaktimestring = secondsToTime(currentBreakTime)
      await asyncio.sleep(breakNotification)
      await ctx.send("```TIMELEFT:  %s```" %breaktimestring)
      currentBreakTime -= breakNotification
    await asyncio.sleep(breakNotification)
    await ctx.send("```DONE```")
    await asyncio.sleep(1)
      
    
    
  


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')



bot.remove_command('help')

@bot.command()
async def help(ctx):
    # title="Welcome to Pomodoro"
    # description="Available Commands:\n!pom start \"minutes for work\" \"minutes for break\" \" number of intervals\" \n!pom pause \n!pom resume \n!pom cancel"
    # embedThis = discord.Embed(title=title, description=description)
    # await ctx.send(embed=embedThis)
  embed=discord.Embed(title="Welcome to PomoDiscordo Timer ✨", description="Get your money up, not your funny up.", color=0x46dde5)
  embed.set_thumbnail(url="https://i.imgur.com/Ei0Uq0d.jpg")
  embed.add_field(name="Get Started With", value="!pom default", inline=True) 
  embed.add_field(name="Need to Stop?:", value="!pom cancel",inline=True)
  embed.add_field(name="Custom Time:", value="!pom start<worktime> <breaktime> <intervals>", inline=False)
  embed.set_footer(icon_url=ctx.author.display_avatar,text="Session begun by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

@bot.command()
async def start(ctx, pomodorot: int, breaktime: int, intervals: int):
  global status
  if status != 1:
    if pomodorot < 0 or pomodorot > 180:
       await ctx.send("Please enter a pomodoro minutes value from 0 to 180")
    
      
    if breaktime < 0 or breaktime > 180:
      await ctx.send("Please enter a break minutes value from 0 to 180")
      
    if intervals < 0 or intervals > 10:
      await ctx.send("Please enter an interval numbers value from 0 to 10")
    else: 
      status = 1
      await pomodoro(pomodorot, breaktime, intervals, ctx)
      

  

  else:
    await ctx.send("Pomodoro in-progress\ntype \"!pom cancel\" to cancel it")
    

@bot.command()
async def default(ctx):
  global status
  if status != 1:
    
    status = 1
    await pomodoro(25, 5, 4, ctx)
  else:
    await ctx.send("Pomodoro in-progress\ntype \"!pom cancel\" to cancel it")

  



@bot.command()
async def pause(ctx):
    global status
    status = False
    await ctx.send("Pomodoro paused")

@bot.command()
async def resume(ctx):
    global resume
    resume = True
    await ctx.send("Pomodoro resumed")

@bot.command()
async def cancel(ctx):
    global status
    if status == 0:
      await ctx.send("No active Pomodoro")
    else:
      status = 0
      await ctx.send("Pomodoro cancelled")

my_secret = os.environ['token']
bot.run(my_secret)