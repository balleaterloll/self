from keep_alive import keep_alive
keep_alive()
import discord
from discord.ext import commands
import ctypes
import json
import os
import random
import requests
import asyncio
import string
import time
import datetime
from colorama import Fore
import platform
import itertools
from gtts import gTTS
import io
import qrcode
import pyfiglet


print("""
    \x1b[38;5;127m  ▄████  ▒█████      ▄▄▄██▀▀▀ ▒█████  
    \x1b[38;5;127m ██▒ ▀█▒▒██▒  ██▒      ▒██  ▒██▒  ██▒
    \x1b[38;5;127m▒██░▄▄▄░▒██░  ██▒      ░██  ▒██░  ██▒
    \x1b[38;5;127m░▓█  ██▓▒██   ██░   ▓██▄██▓ ▒██   ██░
    \x1b[38;5;127m░▒▓███▀▒░ ████▓▒░    ▓███▒  ░ ████▓▒░
    \x1b[38;5;127m ░▒   ▒ ░ ▒░▒░▒░     ▒▓▒▒░  ░ ▒░▒░▒░ 
    \x1b[38;5;127m  ░   ░   ░ ▒ ▒░     ▒ ░▒░    ░ ▒ ▒░ 
    \x1b[38;5;127m░ ░   ░ ░ ░ ░ ▒      ░ ░ ░  ░ ░ ░ ▒  
    \x1b[38;5;127m      ░     ░ ░      ░   ░      ░ ░  
                                                   \n""")
with open("config/config.json", "r") as file:
    config = json.load(file)

# ==================== UNLIMITED TOKENS FROM ENVIRONMENT ====================
tokens = []

# Check main token
main_token = os.environ.get("DISCORD_TOKEN")
if main_token:
    tokens.append(("DISCORD_TOKEN", main_token))

# Check DISCORD_TOKEN_1 to DISCORD_TOKEN_1000 (you can go higher if needed)
for i in range(1, 1001):
    key = f"DISCORD_TOKEN_{i}"
    value = os.environ.get(key)
    if value:
        tokens.append((key, value))
    else:
        # Stop when we don't find the next one (saves time)
        if i > 5:  
            break

if not tokens:
    print("\x1b[38;5;196m[ERROR] No tokens found in Environment Variables!\x1b[0m")
    print("Add DISCORD_TOKEN or DISCORD_TOKEN_1, DISCORD_TOKEN_2 ...")
    exit(1)

print(Fore.GREEN + f"[SUCCESS] Loaded {len(tokens)} token(s) from Environment" + Fore.RESET)
for name, tok in tokens:
    print(Fore.CYAN + f"   • {name} ({len(tok)} chars)" + Fore.RESET)

# Use first token
token = tokens[0][1]
print(Fore.YELLOW + f"[RUNNING] Using {tokens[0][0]}" + Fore.RESET)

prefix = config.get("prefix")
spam_filter = config.get("filter", "")
message_generator = itertools.cycle(config["autoreply"]["messages"])
fillermore_emojis = None

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

__version__ = "3.2"

start_time = datetime.datetime.now(datetime.timezone.utc)

def discord_len(s):
    return sum(2 if ord(c) > 0xFFFF else 1 for c in s)

def save_config(config):
    with open("config/config.json", "w") as file:
        json.dump(config, file, indent=4)


def selfbot_menu(bot):
    if platform.system() == "Windows":
        os.system('cls')
    else:
        # Works for Linux and Termux
        os.system('clear')
    
    # Check for Termux specifically to provide helpful hints
    if "TERMUX_VERSION" in os.environ:
        print("\x1b[38;5;214m[TERMUX]: Detected Termux environment.\x1b[0m")
        print("\x1b[38;5;214m[TIP]: Run 'termux-wake-lock' to keep the bot alive in background.\x1b[0m")
    print("""
    \x1b[38;5;127m  ▄████  ▒█████      ▄▄▄██▀▀▀ ▒█████  
    \x1b[38;5;127m ██▒ ▀█▒▒██▒  ██▒      ▒██  ▒██▒  ██▒
    \x1b[38;5;127m▒██░▄▄▄░▒██░  ██▒      ░██  ▒██░  ██▒
    \x1b[38;5;127m░▓█  ██▓▒██   ██░   ▓██▄██▓ ▒██   ██░
    \x1b[38;5;127m░▒▓███▀▒░ ████▓▒░    ▓███▒  ░ ████▓▒░
    \x1b[38;5;127m ░▒   ▒ ░ ▒░▒░▒░     ▒▓▒▒░  ░ ▒░▒░▒░ 
    \x1b[38;5;127m  ░   ░   ░ ▒ ▒░     ▒ ░▒░    ░ ▒ ▒░ 
    \x1b[38;5;127m░ ░   ░ ░ ░ ░ ▒      ░ ░ ░  ░ ░ ░ ▒  
    \x1b[38;5;127m      ░     ░ ░      ░   ░      ░ ░  
                                                        \n""")

    print(f"""
    https://discord.gg/v2QwrUPUzk
 Linked --> \x1b[38;5;127m {bot.user} \x1b[38;5;255m 
 Gojo Prefix -->\x1b[38;5;127m {prefix}\x1b[38;5;255m
 Nitro Sniper --> \x1b[38;5;48m Enabled \x1b[38;5;255m
 Extra Commands --> \x1b[38;5;48m Enabled \x1b[38;5;255m
 Anti-Ban --> \x1b[38;5;48m Enabled \x1b[38;5;255m
 """)




bot = commands.Bot(command_prefix=prefix, description='not a selfbot', self_bot=True, help_command=None)

@bot.event
async def on_ready():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"SelfBot v{__version__} - Made By Gojo")
        os.system('cls')
    else:
        os.system('clear')
    selfbot_menu(bot)

@bot.event
async def on_message(message):
    if message.author.id in config["copycat"]["users"]:
        if message.content.startswith(config['prefix']):
            response_message = message.content[len(config['prefix']):]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    if config["afk"]["enabled"]:
        if bot.user in message.mentions and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return
        elif isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return

    if message.author != bot.user:
        if str(message.author.id) in config["autoreply"]["users"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
        elif str(message.channel.id) in config["autoreply"]["channels"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return

    if message.guild and message.guild.id == 1279905004181917808 and message.content.startswith(config['prefix']):
        await message.delete()
        await message.channel.send("> SelfBot commands are not allowed here. Thanks.", delete_after=5)
        return

    if message.author != bot.user:
        if str(message.author.id) in config["remote-users"]:
            current_prefix = config.get("prefix", ".")
            if message.content.startswith(current_prefix):
                try:
                    await message.add_reaction("✅")
                    # If there are attachments, we need to send them along with the content
                    if message.attachments:
                        files = []
                        for attachment in message.attachments:
                            file_bytes = await attachment.read()
                            # Use a descriptive filename if possible, otherwise generic
                            fname = attachment.filename or "attachment.png"
                            files.append(discord.File(io.BytesIO(file_bytes), filename=fname))
                        
                        # Use bot.process_commands manually for the sent message content
                        # instead of just echoing it, so the bot sees its own message as a command.
                        # Wait, we can just invoke the command directly if we find it.
                        
                        sent_msg = await message.channel.send(message.content, files=files)
                        # Ensure the bot processes this message as its own command
                        await bot.process_commands(sent_msg)
                    else:
                        sent_msg = await message.channel.send(message.content)
                        await bot.process_commands(sent_msg)
                except Exception:
                    pass
            return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.message.delete()

    help_text1 = f"""
**⚔️ GOJO SELFBOT ⚔️**
**Prefix:** `.` | **Logged in as:** gojojodkabot

**🔧 Utility & Info:**
> `.gojo` - Show social links
> `.ping` - Bot latency
> `.uptime` - Uptime
> `.geoip <ip>` - IP lookup
> `.pingweb <url>` - Website ping
> `.tokeninfo <token>` - Token info
> `.guildinfo` - Server info
> `.qr <text>` - QR Code
> `.tts <text>` - Text to Speech
> `.hidemention <msg>` - Hide mention
> `.gentoken` - Fake token
> `.nitro` - Fake Nitro"""
    await ctx.send(help_text1)

    help_text2 = f"""
**🔥 Spam & Fun:**
> `.spam <amount> <msg>` - Simple spam
> `.targetspam <target>` - Target spam
> `.filler <text>` - Set filler
> `.fillermore <emoji1> <emoji2>` - Emoji spam
> `.ascii <text>` - ASCII art
> `.dick <@user>` - Dick size
> `.leet <text>` - Leetspeak
> `.minesweeper` - Minesweeper game"""
    await ctx.send(help_text2)

    help_text3 = f"""
**🔄 Rename Loops:**
> `.photonc` - Photo loop (2 photos)
> `.gcnc <name>` - Group name loop
> `.profilenc <name>` - Profile name loop
> `.servernc <name>` - Server name loop
> `.targetnc <target>` - Mass name spam
> `.fullnc <target>` - Spammy Fast Nc

**⚙️ Management:**
> `.sudo add/remove @user` - Remote control
> `.afk on/off` - AFK mode
> `.autoreply on/off` - Auto reply
> `.copycat on/off @user` - Copy user
> `.changeprefix <new>` - Change prefix
> `.stopall` - Stops everything

**🚀 Mass:**
> `.dmall <msg>` - DM all members
> `.sendall <msg>` - Send to all channels
> `.purge <amount>` - Delete messages
> `.cleardm` - Clear DMs"""
    await ctx.send(help_text3)

@bot.command()
async def photonc(ctx):
    await ctx.message.delete()
    
    if len(ctx.message.attachments) < 2:
        # Check if the user is a sudo user, they might have sent the command 
        # and the bot might have echoed it without attachments if not handled.
        # But wait, the bot's on_message for sudo users usually just re-sends the content.
        # Let's assume the attachments are present in the context message.
        await ctx.send("> **[ERROR]**: Please attach at least 2 photos to the message.", delete_after=5)
        return

    changing_photos[ctx.channel.id] = True
    
    # Save the photos
    photo_data = []
    for i, attachment in enumerate(ctx.message.attachments[:2]):
        data = await attachment.read()
        photo_data.append(data)
    
    await ctx.send(f"> **Started photo rename loop for this group.**", delete_after=5)
    
    try:
        while changing_photos.get(ctx.channel.id):
            for data in photo_data:
                if not changing_photos.get(ctx.channel.id):
                    break
                try:
                    await ctx.channel.edit(icon=data)
                    # No sleep here for "fucking fast" speed
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                        await asyncio.sleep(retry_after)
                    else:
                        # Continue loop even on 403/400 to keep it "unlimited"
                        pass
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: Photo loop stopped\n> __Error__: `{str(e)}`", delete_after=5)
    finally:
        changing_photos.pop(ctx.channel.id, None)

@bot.command()
async def stopphotonc(ctx):
    await ctx.message.delete()
    changing_photos[ctx.channel.id] = False
    await ctx.send("> **Stopped photo rename loop.**", delete_after=5)

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."

    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    await ctx.send(uptime_stamp)

@bot.command()
async def ping(ctx):
    await ctx.message.delete()

    before = time.monotonic()
    message_to_send = await ctx.send("Pinging...")

    await message_to_send.edit(content=f"`{int((time.monotonic() - before) * 1000)} ms`")

@bot.command(aliases=['Gojo'])
async def gojo(ctx):
    await ctx.message.delete()

    embed = f"""https://guns.lol/notarnavxgojo69"""

    await ctx.send(embed)


@bot.command()
async def geoip(ctx, ip: str=None):
    await ctx.message.delete()

    if not ip:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `geoip <ip>`", delete_after=5)
        return

    try:
        r = requests.get(f'http://ip-api.com/json/{ip}')
        geo = r.json()
        embed = f"""**GEOLOCATE IP | Prefix: `{prefix}`**\n
        > :pushpin: `IP`\n*{geo['query']}*
        > :globe_with_meridians: `Country-Region`\n*{geo['country']} - {geo['regionName']}*
        > :department_store: `City`\n*{geo['city']} ({geo['zip']})*
        > :map: `Latitute-Longitude`\n*{geo['lat']} - {geo['lon']}*
        > :satellite: `ISP`\n*{geo['isp']}*
        > :robot: `Org`\n*{geo['org']}*
        > :alarm_clock: `Timezone`\n*{geo['timezone']}*
        > :electric_plug: `As`\n*{geo['as']}*"""
        await ctx.send(embed, file=discord.File("img/gojo.gif"))
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to geolocate ip\n> __Error__: `{str(e)}`', delete_after=5)


@bot.command()
async def tts(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `tts <message>`", delete_after=5)
        return

    content = content.strip()

    tts = gTTS(text=content, lang="en")

    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)

    await ctx.send(file=discord.File(f, f"{content[:10]}.wav"))

@bot.command(aliases=['qrcode'])
async def qr(ctx, *, text: str="https://discord.gg/PKR7nM9j9U"):
    qr = qrcode.make(text)

    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr)
    img_byte_arr.seek(0)



    await ctx.send(file=discord.File(img_byte_arr, "qr_code.png"))

@bot.command()
async def pingweb(ctx, website_url: str=None):
    await ctx.message.delete()

    if not website_url:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `pingweb <url>`", delete_after=5)
        return

    try:
        r = requests.get(website_url).status_code
        if r == 404:
            await ctx.send(f'> Website **down** *({r})*')
        else:
            await ctx.send(f'> Website **operational** *({r})*')
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to ping website\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def gentoken(ctx, user: str=None):
    await ctx.message.delete()

    code = "ODA"+random.choice(string.ascii_letters)+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))+"."+random.choice(string.ascii_letters).upper()+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))+"."+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))

    if not user:
        await ctx.send(''.join(code))
    else:
        await ctx.send(f"> {user}'s token is: ||{''.join(code)}||")

@bot.command()
async def quickdelete(ctx, *, message: str=None):
    await ctx.message.delete()

    if not message:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `quickdelete <message>`', delete_after=2)
        return

    await ctx.send(message, delete_after=2)

@bot.command(aliases=['uicon'])
async def usericon(ctx, user: discord.User = None):
    await ctx.message.delete()

    if not user:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `usericon <@user>`', delete_after=5)
        return
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    await ctx.send(f"> {user.mention}'s avatar:\n{avatar_url}")


@bot.command(aliases=['tinfo'])
async def tokeninfo(ctx, usertoken: str=None):
    await ctx.message.delete()

    if not usertoken:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `tokeninfo <token>`', delete_after=5)
        return

    headers = {'Authorization': usertoken, 'Content-Type': 'application/json'}
    languages = {
        'da': 'Danish, Denmark',
        'de': 'German, Germany',
        'en-GB': 'English, United Kingdom',
        'en-US': 'English, United States',
        'es-ES': 'Spanish, Spain',
        'fr': 'French, France',
        'hr': 'Croatian, Croatia',
        'lt': 'Lithuanian, Lithuania',
        'hu': 'Hungarian, Hungary',
        'nl': 'Dutch, Netherlands',
        'no': 'Norwegian, Norway',
        'pl': 'Polish, Poland',
        'pt-BR': 'Portuguese, Brazilian, Brazil',
        'ro': 'Romanian, Romania',
        'fi': 'Finnish, Finland',
        'sv-SE': 'Swedish, Sweden',
        'vi': 'Vietnamese, Vietnam',
        'tr': 'Turkish, Turkey',
        'cs': 'Czech, Czechia, Czech Republic',
        'el': 'Greek, Greece',
        'bg': 'Bulgarian, Bulgaria',
        'ru': 'Russian, Russia',
        'uk': 'Ukrainian, Ukraine',
        'th': 'Thai, Thailand',
        'zh-CN': 'Chinese, China',
        'ja': 'Japanese',
        'zh-TW': 'Chinese, Taiwan',
        'ko': 'Korean, Korea'
    }

    try:
        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: An error occurred while sending request\n> __Error__: `{str(e)}`', delete_after=5)
        return

    if res.status_code == 200:
        res_json = res.json()
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_id = res_json['id']
        avatar_id = res_json['avatar']
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
        phone_number = res_json['phone']
        email = res_json['email']
        mfa_enabled = res_json['mfa_enabled']
        flags = res_json['flags']
        locale = res_json['locale']
        verified = res_json['verified']
        days_left = ""
        language = languages.get(locale)
        creation_date = datetime.datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
        has_nitro = False

        try:
            nitro_res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
            nitro_res.raise_for_status()
            nitro_data = nitro_res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                d2 = datetime.datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                days_left = abs((d2 - d1).days)
        except requests.exceptions.RequestException as e:
            pass

        try:
            embed = f"""**TOKEN INFORMATIONS | Prefix: `{prefix}`**\n
        > :dividers: __Basic Information__\n\tUsername: `{user_name}`\n\tUser ID: `{user_id}`\n\tCreation Date: `{creation_date}`\n\tAvatar URL: `{avatar_url if avatar_id else "None"}`
        > :crystal_ball: __Nitro Information__\n\tNitro Status: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`
        > :incoming_envelope: __Contact Information__\n\tPhone Number: `{phone_number if phone_number else "None"}`\n\tEmail: `{email if email else "None"}`
        > :shield: __Account Security__\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tFlags: `{flags}`
        > :paperclip: __Other__\n\tLocale: `{locale} ({language})`\n\tEmail Verified: `{verified}`"""

            await ctx.send(embed, file=discord.File("img/gojo.gif"))
        except Exception as e:
            await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: `{str(e)}`', delete_after=5)
    else:
        await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: Invalid token', delete_after=5)

@bot.command()
async def cleardm(ctx, amount: str="1"):
    await ctx.message.delete()

    if not amount.isdigit():
        await ctx.send(f'> **[**ERROR**]**: Invalid amount specified. It must be a number.\n> __Command__: `{config["prefix"]}cleardm <amount>`', delete_after=5)
        return

    amount = int(amount)

    if amount <= 0 or amount > 100:
        await ctx.send(f'> **[**ERROR**]**: Amount must be between 1 and 100.', delete_after=5)
        return

    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in DMs.', delete_after=5)
        return

    deleted_count = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == bot.user:
            try:
                await message.delete()
                deleted_count += 1
            except discord.Forbidden:
                await ctx.send(f'> **[**ERROR**]**: Missing permissions to delete messages.', delete_after=5)
                return
            except discord.HTTPException as e:
                await ctx.send(f'> **[**ERROR**]**: An error occurred while deleting messages: {str(e)}', delete_after=5)
                return

    await ctx.send(f'> **Cleared {deleted_count} messages in DMs.**', delete_after=5)


@bot.command(aliases=['hs'])
async def hypesquad(ctx, house: str=None):
    await ctx.message.delete()

    if not house:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `hypesquad <house>`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json'}

    try:
        r = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Invalid status code\n> __Error__: `{str(e)}`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
    payload = {}
    if house == "bravery":
        payload = {'house_id': 1}
    elif house == "brilliance":
        payload = {'house_id': 2}
    elif house == "balance":
        payload = {'house_id': 3}
    else:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Error__: Hypesquad house must be one of the following: `bravery`, `brilliance`, `balance`', delete_after=5)
        return

    try:
        r = requests.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        r.raise_for_status()

        if r.status_code == 204:
            await ctx.send(f'> Hypesquad House changed to `{house}`!')

    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to change Hypesquad house\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command(aliases=['ginfo'])
async def guildinfo(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    date_format = "%a, %d %b %Y %I:%M %p"
    embed = f"""> **GUILD INFORMATIONS | Prefix: `{prefix}`**
:dividers: __Basic Information__
Server Name: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nCreation Date: `{ctx.guild.created_at.strftime(date_format)}`\nServer Icon: `{ctx.guild.icon.url if ctx.guild.icon.url else 'None'}`\nServer Owner: `{ctx.guild.owner}`
:page_facing_up: __Other Information__
`{len(ctx.guild.members)}` Members\n`{len(ctx.guild.roles)}` Roles\n`{len(ctx.guild.text_channels) if ctx.guild.text_channels else 'None'}` Text-Channels\n`{len(ctx.guild.voice_channels) if ctx.guild.voice_channels else 'None'}` Voice-Channels\n`{len(ctx.guild.categories) if ctx.guild.categories else 'None'}` Categories"""

    await ctx.send(embed)

@bot.command()
async def nitro(ctx):
    await ctx.message.delete()

    await ctx.send(f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}")

@bot.command()
async def whremove(ctx, webhook: str=None):
    await ctx.message.delete()

    if not webhook:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}whremove <webhook>`', delete_after=5)
        return

    try:
        requests.delete(webhook.rstrip())
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to delete webhook\n> __Error__: `{str(e)}`', delete_after=5)
        return

    await ctx.send(f'> Webhook has been deleted!')

@bot.command(aliases=['hide'])
async def hidemention(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}hidemention <message>`', delete_after=5)
        return

    await ctx.send(content + ('||\u200b||' * 200) + '@everyone')

@bot.command()
async def edit(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}edit <message>`', delete_after=5)
        return

    text = await ctx.send(content)

    await text.edit(content=f"\u202b{content}")

@bot.command(aliases=['911'])
async def airplane(ctx):
    await ctx.message.delete()

    frames = [
        f''':man_wearing_turban::airplane:\t\t\t\t:office:''',
        f''':man_wearing_turban:\t:airplane:\t\t\t:office:''',
        f''':man_wearing_turban:\t\t::airplane:\t\t:office:''',
        f''':man_wearing_turban:\t\t\t:airplane:\t:office:''',
        f''':man_wearing_turban:\t\t\t\t:airplane::office:''',
        ''':boom::boom::boom:''']

    sent_message = await ctx.send(frames[0])

    for frame in frames[1:]:
        await asyncio.sleep(0.5)
        await sent_message.edit(content=frame)


@bot.command(aliases=['mine'])
async def minesweeper(ctx, size: int=5):
    await ctx.message.delete()

    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for _ in range(size - 1)]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
    m_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    message_to_send = "**Click to play**:\n"

    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offsets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message_to_send += tile
        message_to_send += "\n"

    await ctx.send(message_to_send)

@bot.command(aliases=['leet'])
async def leetspeak(ctx, *, content: str):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `leetspeak <message>`", delete_after=5)
        return

    content = content.replace('a', '4').replace('A', '4').replace('e', '3').replace('E', '3').replace('i', '1').replace('I', '1').replace('o', '0').replace('O', '0').replace('t', '7').replace('T', '7').replace('b', '8').replace('B', '8')
    await ctx.send(content)

@bot.command()
async def dick(ctx, user: str=None):
    await ctx.message.delete()

    if not user:
        user = ctx.author.display_name

    size = random.randint(1, 15)
    dong = "=" * size

    await ctx.send(f"> **{user}**'s Dick size\n8{dong}D")

@bot.command()
async def reverse(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `reverse <message>`", delete_after=5)
        return

    content = content[::-1]
    await ctx.send(content)

@bot.command(aliases=['fetch'])
async def fetchmembers(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in a server.', delete_after=5)
        return

    members = ctx.guild.members
    member_data = []

    for member in members:
        member_info = {
            "name": member.name,
            "id": str(member.id),
            "avatar_url": str(member.avatar.url) if member.avatar else str(member.default_avatar.url),
            "discriminator": member.discriminator,
            "status": str(member.status),
            "joined_at": str(member.joined_at)
        }
        member_data.append(member_info)

    with open("members_list.json", "w", encoding="utf-8") as f:
        json.dump(member_data, f, indent=4)

    await ctx.send("> List of members:", file=discord.File("members_list.json"))

    os.remove("members_list.json")

@bot.command()
async def spam(ctx, amount: int=1, *, message_to_send: str="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    try:
        tasks = [ctx.send(message_to_send) for _ in range(amount)]
        await asyncio.gather(*tasks)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: `{str(e)}`', delete_after=5)

@bot.command(aliases=['gicon'])
async def guildicon(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} icon :**\n{ctx.guild.icon.url if ctx.guild.icon else '*NO ICON*'}")

@bot.command(aliases=['gbanner'])
async def guildbanner(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} banner :**\n{ctx.guild.banner.url if ctx.guild.banner else '*NO BANNER*'}")

server_ncs = {}

@bot.command(aliases=['grename', 'servernc'])
async def guildrename(ctx, *, name: str=None):
    await ctx.message.delete()

    if not name:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `servernc <name>`", delete_after=5)
        return

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.guild.me.guild_permissions.manage_guild:
        await ctx.send(f'> **[**ERROR**]**: Missing permissions', delete_after=5)
        return

    if ctx.guild.id in server_ncs:
        await ctx.send("> **[ERROR]**: Server rename loop is already running.", delete_after=5)
        return

    server_ncs[ctx.guild.id] = True
    emojis = [
        "🤣", "😭", "💀", "🔥", "💯", "👑", "🤡", "💖", "✨", "🚀", 
        "😂", "🥺", "🥶", "😡", "😈", "👺", "🤡", "🤖", "👻", "👽",
        "💩", "🔥", "💨", "💦", "⚡", "🌟", "💢", "💎", "🔫", "🧿"
    ]

    await ctx.send(f"> Started server rename loop for `{name}`", delete_after=5)

    try:
        while server_ncs.get(ctx.guild.id):
            for emoji in emojis:
                if not server_ncs.get(ctx.guild.id):
                    break
                try:
                    await ctx.guild.edit(name=f"{name} ({emoji})")
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 15
                        await asyncio.sleep(retry_after)
                    else:
                        raise e
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: Server rename loop stopped\n> __Error__: `{str(e)}`", delete_after=5)
    finally:
        server_ncs.pop(ctx.guild.id, None)

@bot.command()
async def stopservernc(ctx):
    await ctx.message.delete()
    if ctx.guild.id in server_ncs:
        server_ncs[ctx.guild.id] = False
    await ctx.send("> **Stopped server rename loop.**", delete_after=5)

@bot.command()
async def purge(ctx, num_messages: int=1):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("> **[**ERROR**]**: You do not have permission to delete messages", delete_after=5)
        return

    if 1 <= num_messages <= 100:
        deleted_messages = await ctx.channel.purge(limit=num_messages)
        await ctx.send(f"> **{len(deleted_messages)}** messages have been deleted", delete_after=5)
    else:
        await ctx.send("> **[**ERROR**]**: The number must be between 1 and 100", delete_after=5)

@bot.command(aliases=['autor'])
async def autoreply(ctx, command: str, user: discord.User=None):
    await ctx.message.delete()

    if command not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid input. Use `ON` or `OFF`.\n> __Command__: `autoreply ON|OFF [@user]`", delete_after=5)
        return

    if command.upper() == "ON":
        if user:
            if str(user.id) not in config["autoreply"]["users"]:
                config["autoreply"]["users"].append(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply enabled for user {user.mention}.**", delete_after=5)
        else:
            if str(ctx.channel.id) not in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].append(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been enabled in this channel**", delete_after=5)
    elif command.upper() == "OFF":
        if user:
            if str(user.id) in config["autoreply"]["users"]:
                config["autoreply"]["users"].remove(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply disabled for user {user.mention}**", delete_after=5)
        else:
            if str(ctx.channel.id) in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].remove(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been disabled in this channel**", delete_after=5)

@bot.command(aliases=['remote'])
async def sudo(ctx, action: str = None, user: discord.User = None):
    await ctx.message.delete()

    # ==================== AUTO SUDO FOR OWNERS ====================
    owner_ids = config.get("owner_ids", [])
    if ctx.author.id in [int(x) for x in owner_ids]:
        # Owner hai toh direct sudo power de do (no need to add in remote-users)
        pass
    elif str(ctx.author.id) not in config.get("remote-users", []):
        await ctx.send("> **❌ Only Owner or Sudo Users can use this command.**", delete_after=5)
        return
    # ============================================================

    if not action:
        await ctx.send(f"> Usage: `{prefix}sudo add/remove @user`", delete_after=5)
        return

    action = action.upper()

    if action == "ADD" and user:
        user_id_str = str(user.id)
        if user_id_str not in config.get("remote-users", []):
            config.setdefault("remote-users", []).append(user_id_str)
            save_config(config)
            await ctx.send(f"> **✅ {user.mention} added as Sudo User**", delete_after=5)
        else:
            await ctx.send(f"> **ℹ️ Already Sudo**", delete_after=5)

    elif action == "REMOVE" and user:
        user_id_str = str(user.id)
        if user_id_str in config.get("remote-users", []):
            config["remote-users"].remove(user_id_str)
            save_config(config)
            await ctx.send(f"> **✅ {user.mention} removed from Sudo**", delete_after=5)
        else:
            await ctx.send(f"> **Not in Sudo**", delete_after=5)
    else:
        await ctx.send(f"> Usage: `{prefix}sudo add/remove @user`", delete_after=5)
@bot.command()
async def afk(ctx, status: str, *, message: str=None):
    await ctx.message.delete()

    if status not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `afk ON|OFF <message>`", delete_after=5)
        return

    if status.upper() == "ON":
        if not config["afk"]["enabled"]:
            config["afk"]["enabled"] = True
            if message:
                config["afk"]["message"] = message
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> **AFK mode enabled.** Message: `{config['afk']['message']}`", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is already enabled", delete_after=5)
    elif status.upper() == "OFF":
        if config["afk"]["enabled"]:
            config["afk"]["enabled"] = False
            save_config(config)
            selfbot_menu(bot)
            await ctx.send("> **AFK mode disabled.** Welcome back!", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is not currently enabled", delete_after=5)

@bot.command(aliases=["prefix"])
async def changeprefix(ctx, *, new_prefix: str=None):
    await ctx.message.delete()

    if not new_prefix:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `changeprefix <prefix>`", delete_after=5)
        return

    config['prefix'] = new_prefix
    save_config(config)
    selfbot_menu(bot)

    bot.command_prefix = new_prefix

    await ctx.send(f"> Prefix updated to `{new_prefix}`", delete_after=5)

@bot.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()

    msg = await ctx.send("> Shutting down...")
    await asyncio.sleep(2)

    await msg.delete()
    await bot.close()

@bot.command()
async def clear(ctx):
    await ctx.message.delete()

    await ctx.send('ﾠﾠ' + '\n' * 200 + 'ﾠﾠ')

@bot.command()
async def sendall(ctx, *, message="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    channels = ctx.guild.text_channels
    success_count = 0
    failure_count = 0

    try:        
        for channel in channels:
            try:
                await channel.send(message)
                success_count += 1
            except Exception as e:
                failure_count += 1
        await ctx.send(f"> {success_count} message(s) sent successfully, {failure_count} failed to send", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[**ERROR**]**: An error occurred: `{e}`", delete_after=5)

@bot.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, action: str=None, user: discord.User=None):
    await ctx.message.delete()

    if action not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return

    if not user:
        await ctx.send(f"> **[**ERROR**]**: Please specify a user to copy.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return

    if action == "ON":
        if user.id not in config['copycat']['users']:
            config['copycat']['users'].append(user.id)
            save_config(config)
            await ctx.send(f"> Now copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` is already being copied.", delete_after=5)

    elif action == "OFF":
        if user.id in config['copycat']['users']:
            config['copycat']['users'].remove(user.id)
            save_config(config)
            await ctx.send(f"> Stopped copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` was not being copied.", delete_after=5)

@bot.command()
async def firstmessage(ctx):
    await ctx.message.delete()

    try:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}"
            await ctx.send(f"> Here is the link to the first message: {link}", delete_after=5)
            break
        else:
            await ctx.send("> **[ERROR]**: No messages found in this channel.", delete_after=5)

    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while fetching the first message. `{e}`", delete_after=5)

@bot.command()
async def ascii(ctx, *, message=None):
    await ctx.message.delete()

    if not message:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `ascii <message>`", delete_after=5)
        return

    try:
        ascii_art = pyfiglet.figlet_format(message)
        await ctx.send(f"```\n{ascii_art}\n```", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while generating the ASCII art. `{e}`", delete_after=5)


@bot.command()
async def playing(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `playing <status>`", delete_after=5)
        return

    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"> Successfully set the game status to `{status}`", delete_after=5)

@bot.command()
async def streaming(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `streaming <status>`", delete_after=5)
        return

    await bot.change_presence(activity=discord.Streaming(name=status, url=f"https://www.twitch.tv/{status}"))
    await ctx.send(f"> Successfully set the streaming status to `{status}`", delete_after=5)

@bot.command(aliases=["stopstreaming", "stopstatus", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()

    await bot.change_presence(activity=None, status=discord.Status.dnd)

@bot.command()
async def dmall(ctx, *, message: str="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    members = [m for m in ctx.guild.members if not m.bot]
    total_members = len(members)
    estimated_time = round(total_members * 4.5)


    await ctx.send(f">Starting DM process for `{total_members}` members.\n> Estimated time: `{estimated_time} seconds` (~{round(estimated_time / 60, 2)} minutes)", delete_after=10)

    success_count = 0
    fail_count = 0

    for member in members:
        try:
            await member.send(message)
            success_count += 1
        except Exception:
            fail_count += 1

        await asyncio.sleep(random.uniform(3, 6))

    await ctx.send(f"> **[**INFO**]**: DM process completed.\n> Successfully sent: `{success_count}`\n> Failed: `{fail_count}`", delete_after=10)


target_spamming = {}
changing_gcs = {}
changing_photos = {}

@bot.command()
async def targetspam(ctx, *, target: str = None):
    await ctx.message.delete()
    if not target:
        await ctx.send("> **[ERROR]**: `.targetspam <target>`", delete_after=5)
        return

    target_spamming[ctx.channel.id] = True
    await ctx.send(f"> **ULTIMATE Target Spam Started** for `{target}`", delete_after=5)

    # 🔥 Updated Abusive Words
    base_templates = [
        f"{target} BHOSDIKE", f"{target} MADARCHOD", f"{target} TMKC",
        f"{target} TERI MAA KI CHUT", f"{target} TERI BEHEN KA BHOSDA",
        f"{target} TERI MAA RANDI", f"{target} BETICHOD", f"{target} RNDYKE",
        f"{target} TERI MAA CHUDKE ROI", f"{target} LAUDE KE BAL",
        f"{target} GANDU", f"{target} CHUT KA BHOSDA", f"{target} BKL",
        f"{target} MC BC", f"{target} HARAMI", f"{target} SUAR KA BACHA",
        f"{target} CHODU", f"{target} LAVDE", f"{target} TERI BHEN KO CHODA",
        f"{target} 6KKE", f"{target} TMKB", f"{target} PY FILE CHAIYE RNDYKE",
        f"{target} JALDI CHUDKE HAT", f"{target} TERI MAA KI CHUT KAALI",
        f"{target} GOJO NE TERI MAA CHODI", f"{target} BAAP KO BOL",
        f"{target} NALLA", f"{target} CHUTIYA", f"{target} BHENCHOD",
        f"{target} MAA KI CHUT ME LUND", f"{target} RANDI KA BACHA",
        f"{target} GAAND ME LUND", f"{target} TERE BAAP KA LUND",
        f"{target} CHODU KE BACHE", f"{target} TERI MAA KO PEL DUNGA",
        f"{target} BEHEN KE LODE", f"{target} GAAND CHAT", f"{target} MUH ME LE",
        f"{target} CHUT MAR", f"{target} BHOSDI KE", f"{target} HARAMI KE BACHE",
        f"{target} TERE KO CHODUNGA", f"{target} TERI MAA KI CHUT FAT GAYI",
        f"{target} TERE BAAP KI GAAND", f"{target} CHODU MADARCHOD",
        f"{target} BEHENCHOD KE", f"{target} TERI MAA KA BHOSDA"
    ]

    try:
        emoji_index = 0
        while target_spamming.get(ctx.channel.id):
            for base in base_templates:
                if not target_spamming.get(ctx.channel.id):
                    break

                if fillermore_emojis and len(fillermore_emojis) > 0:
                    current_emoji = fillermore_emojis[emoji_index % len(fillermore_emojis)]
                    max_repeat = (1980 - len(base)) // len(current_emoji)
                    filler_part = current_emoji * max(12, max_repeat)
                    msg = filler_part + " " + base + " 😈💢"
                    emoji_index += 1
                elif spam_filter:
                    max_repeat = (1980 - len(base)) // len(spam_filter)
                    msg = (spam_filter * max(12, max_repeat)) + " " + base + " 😈💢"
                else:
                    msg = base + " 😈💢"

                try:
                    await ctx.send(msg)
                    await asyncio.sleep(0.22)
                except discord.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after or 1)
    finally:
        target_spamming.pop(ctx.channel.id, None)

@bot.command()
async def filler(ctx, *, content: str = None):
    await ctx.message.delete()
    global spam_filter
    if not content:
        spam_filter = ""
        config["filter"] = ""
        save_config(config)
        await ctx.send("> **Filler cleared.**", delete_after=5)
        return
    spam_filter = content
    config["filter"] = content
    save_config(config)
    await ctx.send(f"> **Filler set to:** `{content}`", delete_after=5)

@bot.command()
async def fillermore(ctx, *, emojis: str = None):
    await ctx.message.delete()
    global fillermore_emojis
    if not emojis:
        fillermore_emojis = None
        await ctx.send("> **Fillermore cleared.**", delete_after=5)
        return
    parts = [e for e in emojis.strip().split(" ") if e]
    if len(parts) < 2:
        await ctx.send("> **[ERROR]**: Give at least 2 emojis separated by a space. Example: `.fillermore 🙏 ⚡️`", delete_after=7)
        return
    fillermore_emojis = tuple(parts)
    preview = " ".join(parts)
    await ctx.send(f"> fillermore activated {preview}")

@bot.command()
async def targetspamstop(ctx):
    await ctx.message.delete()
    if ctx.channel.id in target_spamming:
        target_spamming[ctx.channel.id] = False
    await ctx.send("> **✅ Target Spam stopped.**", delete_after=5)

@bot.command()
async def gcnc(ctx, *, name: str = None):
    await ctx.message.delete()

    if not name:
        await ctx.send(f"> **[ERROR]**: Invalid command.\n> __Command__: `{prefix}gcnc <new_name>`", delete_after=5)
        return

    # Remove the GroupChannel check to allow it in servers too if the user wants,
    # or at least make sure it doesn't fail silently.
    
    changing_gcs[ctx.channel.id] = True
    emojis = ["🤣", "😭", "💀", "🔥", "💯", "👑", "🤡", "💖", "✨", "🚀", "😂", "🥺", "🥶", "😡", "😈", "👺", "🤖", "👻", "👽", "💩", "💨", "💦", "⚡", "🌟", "💢", "💎", "🔫", "🧿"]
    
    await ctx.send(f"> Started rename loop for `{name}`", delete_after=5)
    
    try:
        while changing_gcs.get(ctx.channel.id):
            for emoji in emojis:
                if not changing_gcs.get(ctx.channel.id):
                    break
                try:
                    # Simulating the settings rename by directly editing the channel name
                    # Using the hy (emoji) format as requested
                    await ctx.channel.edit(name=f"{name} ({emoji})")
                    await asyncio.sleep(0.9) 
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 15
                        await asyncio.sleep(retry_after)
                    else:
                        raise e
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: Rename loop stopped\n> __Error__: `{str(e)}`", delete_after=5)
    finally:
        changing_gcs.pop(ctx.channel.id, None)


@bot.command()
async def targetnc(ctx, *, target: str=None):
    await ctx.message.delete()
    if not target:
        await ctx.send("> **[ERROR]**: `.targetnc <target>`", delete_after=5)
        return

    changing_gcs[ctx.channel.id] = True
    await ctx.send(f"> **Target NC Started** for `{target}`", delete_after=5)

    templates = [f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ {i}X ᥇ꪖꪖ᥅ 😈💢" for i in range(1, 1001)]

    try:
        while changing_gcs.get(ctx.channel.id, False):
            for name in templates:
                if not changing_gcs.get(ctx.channel.id, False):
                    break
                try:
                    await ctx.channel.edit(name=name)
                except discord.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after or 1)
                    else:
                        await asyncio.sleep(0.3)
    except:
        pass
    finally:
        changing_gcs.pop(ctx.channel.id, None)
        
@bot.command()
async def stopgcnc(ctx):
    await ctx.message.delete()
    global gcnc_active
    gcnc_active = False
    
    if ctx.channel.id in changing_gcs:
        changing_gcs[ctx.channel.id] = False

    msg = await ctx.send("> **✅ GCNC & TargetNC Stopped**")
    await msg.add_reaction("✅")

profilenc_active = False

@bot.command()
async def profilenc(ctx, *, name: str = None):
    await ctx.message.delete()
    if not name:
        await ctx.send(f"> **[ERROR]**: Invalid input\n> __Command__: `{prefix}profilenc <name>`", delete_after=5)
        return

    global profilenc_active
    profilenc_active = True
    
    emojis = ["🌊", "⚡️", "🔥", "💎", "🌟", "✨", "🩸", "🌀", "🧿", "🚀", "👑", "👺", "💀", "👻", "👽", "👾", "🤖", "🎃", "🪐", "🌑", "🌓", "🌕", "🌘", "⭐", "💫", "🌠", "☄️", "🎇", "🎆", "🌉"]
    
    await ctx.send(f"> **Started profile rename loop for: `{name}`**", delete_after=5)
    
    try:
        while profilenc_active:
            random.shuffle(emojis)
            for emoji in emojis:
                if not profilenc_active:
                    break
                try:
                    # Self-bots often use 'nick' for server-specific or directly hit the API for global name.
                    # Given the library limitations, we will try to update the user's nickname in the current server if possible.
                    if ctx.guild:
                        await ctx.author.edit(nick=f"{name} {emoji}")
                    else:
                        # Fallback for DMs - we can't easily change global display name without the correct keyword
                        # We'll try one more common variant for the library
                        await bot.user.edit(display_name=f"{name} {emoji}")
                    await asyncio.sleep(0.5) 
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 15
                        await asyncio.sleep(retry_after)
                    else:
                        profilenc_active = False
                        break
    except Exception as e:
        print(f"Profile NC Error: {e}")
    finally:
        profilenc_active = False

@bot.command()
async def stopprofilenc(ctx):
    await ctx.message.delete()
    global profilenc_active
    profilenc_active = False
    await ctx.send("> **Stopped profile rename loop.**", delete_after=5)

@bot.command()
async def stopall(ctx):
    await ctx.message.delete()

    # Permission Check
    owner_ids = config.get("owner_ids", [])
    is_owner = ctx.author.id in [int(x) for x in owner_ids]
    is_sudo = str(ctx.author.id) in config.get("remote-users", [])

    if not (is_owner or is_sudo):
        await ctx.send("> **❌ Only Owner or Sudo can use this.**", delete_after=5)
        return

    # STOP EVERYTHING
    global gcnc_active, profilenc_active, fullnc_active
    gcnc_active = False
    profilenc_active = False
    fullnc_active = False

    # Force stop all loops
    changing_gcs.clear()
    target_spamming.clear()
    changing_photos.clear()
    server_ncs.clear()

    stop_msg = await ctx.send("> **🛑 ALL LOOPS & SPAMS HAVE BEEN FORCE STOPPED**")
    await stop_msg.add_reaction("✅")

    print("[STOPALL] All loops forcefully stopped.")

fullnc_active = False

fullnc_active = False

fullnc_active = False

@bot.command()
async def fullnc(ctx, *, target: str = None):
    await ctx.message.delete()
    if not target:
        await ctx.send("> **[ERROR]**: `.fullnc <target>`", delete_after=5)
        return

    global fullnc_active
    fullnc_active = True

    await ctx.send(f"> **FULL NC Started** for `{target}` | Maximum Spam Mode", delete_after=5)

    hearts = ["(🤍)", "(💗)", "(❤️)", "(💖)", "(💘)", "(💝)", "(🩷)", "(💓)", "(💞)","(💔)","(🖤)","(💙)","(💜)"]

    try:
        while fullnc_active:
            for heart in hearts:
                if not fullnc_active:
                    break
                name = f"{target} TERI MAA KA BHOSDA 🤢👞🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀🔥💀 {heart}"
                try:
                    await ctx.channel.edit(name=name)
                except discord.HTTPException as e:
                    if e.status == 429:
                        await asyncio.sleep(e.retry_after or 0.7)
                    else:
                        await asyncio.sleep(0.35)
    except:
        pass
    finally:
        fullnc_active = False


@bot.command()
async def stopfullnc(ctx):
    await ctx.message.delete()
    global fullnc_active
    fullnc_active = False
    await ctx.send("> **✅ Full NC Stopped Successfully**", delete_after=5)

bot.run(token)

