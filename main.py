# This example requires the 'message_content' intent.
import discord
from discord.ext import commands
import os
import asyncio

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
  

async def pomodoro(pomodorotime, breaktime, ctx):
  pomodorotime = minutesToSeconds(pomodorotime)
  notification = pomodorotime / 4 
  timestring = secondsToTime(pomodorotime)
  await ctx.send("```TIMELEFT:  %s```" %timestring)
  pomodorotime -= notification
  while pomodorotime > 0:
    timestring = secondsToTime(pomodorotime)
    await asyncio.sleep(notification)
    await ctx.send("```TIMELEFT:  %s```" %timestring)
    pomodorotime -= notification
  await ctx.send("```DONE  ```")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')



bot.remove_command('help')

@bot.command()
async def help(ctx):
    title="Welcome to Pomodoro"
    description="Available Commands:\n!pom start \"minutes for work\" \"minutes for break\" \n!pom pause \n!pom resume \n!pom cancel"
    embedThis = discord.Embed(title=title, description=description)
    await ctx.send(embed=embedThis)

@bot.command()
async def start(ctx, pomodorot: int, breaktime: int):
   await pomodoro(pomodorot, breaktime, ctx)
    

  
@bot.command()
async def pause(ctx):
    await ctx.send("Pomodoro paused")

@bot.command()
async def resume(ctx):
    await ctx.send("Pomodoro resumed")

@bot.command()
async def cancel(ctx):
    await ctx.send("Pomodoro cancelled")


# @bot.command()
# async def kennytest(ctx):
#     await ctx.send("```css\n [w]```")



# @bot.command()
# async def add(ctx, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# @bot.command()
# async def roll(ctx, dice: str):
#     """Rolls a dice in NdN format."""
#     try:
#         rolls, limit = map(int, dice.split('d'))
#     except Exception:
#         await ctx.send('Format has to be in NdN!')
#         return

#     result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)


# @bot.command(description='For when you wanna settle the score some other way')
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.
#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


# @cool.command(name='bot')
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send('Yes, the bot is cool.') 

my_secret = os.environ['token']
bot.run(my_secret)