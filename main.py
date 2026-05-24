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

# ==================== DYNAMIC MULTI TOKEN SUPPORT ====================
tokens = []

# Check main token
if os.environ.get("DISCORD_TOKEN"):
    tokens.append(("DISCORD_TOKEN", os.environ.get("DISCORD_TOKEN")))

# Check DISCORD_TOKEN_1 to DISCORD_TOKEN_50 (you can increase if needed)
for i in range(1, 51):
    key = f"DISCORD_TOKEN_{i}"
    value = os.environ.get(key)
    if value:
        tokens.append((key, value))

if not tokens:
    print("\x1b[38;5;196m[ERROR] No token found! Set DISCORD_TOKEN or DISCORD_TOKEN_1, DISCORD_TOKEN_2 etc.\x1b[0m")
    exit(1)

print(Fore.GREEN + f"[SUCCESS] Loaded {len(tokens)} token(s)" + Fore.RESET)
for name, tok in tokens:
    print(Fore.CYAN + f"   • {name} ({len(tok)} characters)" + Fore.RESET)

# Use the first token
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
        ctypes.windll.kernel32.SetConsoleTitleW(f"SelfBot v{__version__} - Made By a5traa")
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

    embed = discord.Embed(
        title="⚔️ **GOJO SELFBOT** ⚔️",
        description=f"**Prefix:** `{prefix}`\n**Logged in as:** {bot.user}",
        color=0x9B59B6
    )

    embed.add_field(name="🔧 **Utility**", 
                    value="`ping` `uptime` `gojo` `geoip` `pingweb` `tokeninfo` `guildinfo` `usericon` `qr` `tts`", 
                    inline=False)

    embed.add_field(name="🎨 **Fun**", 
                    value="`ascii` `dick` `leet` `minesweeper` `reverse`", 
                    inline=False)

    embed.add_field(name="🔥 **Spam**", 
                    value="`spam` `targetspam` `filler` `fillermore`", 
                    inline=False)

    embed.add_field(name="🔄 **Rename Loops**", 
                    value="`photonc` `gcnc` `profilenc` `servernc` `targetnc`", 
                    inline=False)

    embed.add_field(name="⚙️ **Management**", 
                    value="`sudo` `afk` `autoreply` `copycat` `changeprefix`", 
                    inline=False)

    embed.add_field(name="🚀 **Mass**", 
                    value="`dmall` `sendall` `purge` `cleardm` `clear`", 
                    inline=False)

    embed.add_field(name="🎮 **Status**", 
                    value="`playing` `streaming` `stopactivity`", 
                    inline=False)

    embed.set_footer(text="Only Owners can use dangerous commands")

    await ctx.send(embed=embed)
    
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

@bot.command(aliases=['astra'])
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

    # ==================== MULTIPLE OWNER CHECK ====================
    owner_ids = config.get("owner_ids", [])
    if not owner_ids:
        owner_ids = [config.get("owner_id")] if config.get("owner_id") else []

    if ctx.author.id not in [int(oid) for oid in owner_ids]:
        await ctx.send("> **❌ Only Owners can use this command.**", delete_after=5)
        return
    # ============================================================

    if not action:
        await ctx.send(f"> **[ERROR]**: Invalid usage.\n> `{prefix}sudo add/remove @user`", delete_after=5)
        return

    action = action.upper()

    if action == "ADD":
        if not user:
            await ctx.send(f"> **[ERROR]**: Mention a user.\n> Example: `{prefix}sudo add @user`", delete_after=5)
            return
        user_id_str = str(user.id)
        if user_id_str not in config.get("remote-users", []):
            config.setdefault("remote-users", []).append(user_id_str)
            save_config(config)
            await ctx.send(f"> **✅ {user.mention} added as Sudo User**", delete_after=5)
        else:
            await ctx.send(f"> **ℹ️ {user.mention} is already a Sudo User**", delete_after=5)

    elif action == "REMOVE":
        if not user:
            await ctx.send(f"> **[ERROR]**: Mention a user.\n> Example: `{prefix}sudo remove @user`", delete_after=5)
            return
        user_id_str = str(user.id)
        if user_id_str in config.get("remote-users", []):
            config["remote-users"].remove(user_id_str)
            save_config(config)
            await ctx.send(f"> **✅ {user.mention} removed from Sudo Users**", delete_after=5)
        else:
            await ctx.send(f"> **ℹ️ {user.mention} was not a Sudo User**", delete_after=5)

    else:
        await ctx.send(f"> **[ERROR]**: Use `add` or `remove`.\n> Example: `{prefix}sudo add @user`", delete_after=5)
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
        await ctx.send(f"> **[ERROR]**: Invalid input\n> __Command__: `{prefix}targetspam <target>`", delete_after=5)
        return

    target_spamming[ctx.channel.id] = True
    templates = [
        f"{target} BHOSDIKE 😈💢",
        f"{target} TMR 😈💢",
        f"{target} MADARCHOD 😈💢",
        f"{target} 6KKE 😈💢",
        f"{target} TMKC ME BUS 😈💢",
        f"{target} RNDYKE CUDKE RO 😈💢",
        f"{target} TMKB 😈💢",
        f"{target} TERI MAA KI CHUT KAALI 😈💢",
        f"{target} BETA GOJO ON TOP BOLO 😈💢",
        f"{target} TERI BHEN KA BHOSDA 😈💢",
        f"{target} TERI BHEN KO LODA CHUSNE DETA HU 😈💢",
        f"{target} PY FILE CHAIYE RNDYKE? 😈💢",
        f"{target} TERI MAA AUR MERI LOVE STORY 😈💢",
        f"{target} TERI MAA CHUDKE ROI 😈💢",
        f"{target} DUSRA NUMBER TERA H AB CHUD 😈💢",
        f"{target} JALDI WAHA SE CHUDKE HAT 😈💢",
        f"{target} LAUDE 😈💢",
        f"{target} GANDU 😈💢",
        f"{target} RO 😈💢",
        f"{target} DFN 😈💢"
    ]

    await ctx.send(f"> Started target spam for `{target}`", delete_after=5)

    try:
        global spam_filter, fillermore_emojis
        send_index = 0
        while target_spamming.get(ctx.channel.id):
            for template in templates:
                if not target_spamming.get(ctx.channel.id):
                    break
                try:
                    if fillermore_emojis:
                        emoji = fillermore_emojis[send_index % len(fillermore_emojis)]
                        max_fill = 1999 - discord_len(template) - 1
                        repeat_count = max(1, max_fill // discord_len(emoji))
                        msg = (emoji * repeat_count) + " " + template
                        send_index += 1
                    elif spam_filter:
                        max_filter_len = 1999 - discord_len(template) - 1
                        repeat_count = max(1, max_filter_len // discord_len(spam_filter))
                        msg = (spam_filter * repeat_count) + " " + template
                    else:
                        msg = template
                    await ctx.send(msg)
                    await asyncio.sleep(0.3)
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                        await asyncio.sleep(retry_after)
                    else:
                        raise e
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: Target spam stopped\n> __Error__: `{str(e)}`", delete_after=5)
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
    await ctx.send("> **Stopped target spam.**", delete_after=5)

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
        await ctx.send(f"> **[ERROR]**: Invalid input\n> __Command__: `{prefix}targetnc <target>`", delete_after=5)
        return

    templates = [
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 1X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 2X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 3X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 4X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 5X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 6X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 7X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 8X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 9X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 10X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 11X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 12X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 13X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 14X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 15X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 16X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 17X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 18X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 19X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 20X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 21X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 22X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 23X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 24X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 25X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 26X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 27X ᥇ꪖꪖ᥅ 😈💢",
        f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 28X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 28X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 29X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 30X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 31X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 32X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 33X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 34X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 35X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 36X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 37X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 38X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 39X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 40X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 41X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 42X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 43X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 44X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 45X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 46X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 47X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 48X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 49X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 50X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 51X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 52X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 53X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 54X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 55X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 56X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 57X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 58X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 59X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 60X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 61X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 62X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 63X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 64X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 65X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 66X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 67X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 68X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 69X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 70X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 71X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 72X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 73X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 74X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 75X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 76X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 77X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 78X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 79X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 80X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 81X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 82X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 83X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 84X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 85X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 86X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 87X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 88X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 89X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 90X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 91X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 92X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 93X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 94X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 95X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 96X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 97X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 98X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 99X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 100X ᥇ꪖꪖ᥅ 😈💢",
f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 101X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 102X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 103X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 104X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 105X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 106X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 107X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 108X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 109X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 110X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 111X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 112X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 113X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 114X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 115X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 116X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 117X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 118X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 119X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 120X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 121X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 122X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 123X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 124X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 125X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 126X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 127X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 128X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 129X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 130X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 131X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 132X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 133X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 134X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 135X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 136X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 137X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 138X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 139X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 140X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 141X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 142X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 143X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 144X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 145X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 146X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 147X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 148X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 149X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 150X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 151X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 152X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 153X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 154X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 155X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 156X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 157X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 158X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 159X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 160X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 161X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 162X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 163X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 164X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 165X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 166X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 167X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 168X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 169X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 170X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 171X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 172X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 173X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 174X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 175X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 176X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 177X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 178X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 179X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 180X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 181X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 182X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 183X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 184X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 185X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 186X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 187X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 188X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 189X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 190X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 191X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 192X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 193X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 194X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 195X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 196X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 197X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 198X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 199X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 200X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 201X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 202X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 203X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 204X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 205X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 206X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 207X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 208X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 209X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 210X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 211X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 212X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 213X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 214X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 215X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 216X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 217X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 218X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 219X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 220X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 221X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 222X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 223X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 224X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 225X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 226X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 227X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 228X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 229X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 230X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 231X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 232X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 233X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 234X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 235X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 236X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 237X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 238X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 239X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 240X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 241X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 242X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 243X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 244X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 245X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 246X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 247X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 248X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 249X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 250X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 251X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 252X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 253X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 254X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 255X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 256X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 257X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 258X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 259X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 260X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 261X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 262X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 263X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 264X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 265X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 266X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 267X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 268X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 269X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 270X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 271X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 272X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 273X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 274X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 275X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 276X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 277X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 278X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 279X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 280X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 281X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 282X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 283X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 284X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 285X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 286X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 287X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 288X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 289X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 290X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 291X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 292X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 293X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 294X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 295X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 296X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 297X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 298X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 299X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 300X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 301X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 302X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 303X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 304X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 305X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 306X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 307X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 308X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 309X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 310X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 311X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 312X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 313X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 314X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 315X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 316X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 317X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 318X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 319X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 320X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 321X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 322X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 323X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 324X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 325X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 326X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 327X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 328X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 329X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 330X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 331X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 332X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 333X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 334X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 335X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 336X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 337X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 338X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 339X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 340X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 341X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 342X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 343X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 344X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 345X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 346X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 347X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 348X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 349X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 350X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 351X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 352X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 353X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 354X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 355X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 356X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 357X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 358X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 359X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 360X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 361X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 362X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 363X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 364X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 365X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 366X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 367X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 368X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 369X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 370X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 371X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 372X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 373X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 374X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 375X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 376X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 377X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 378X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 379X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 380X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 381X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 382X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 383X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 384X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 385X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 386X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 387X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 388X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 389X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 390X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 391X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 392X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 393X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 394X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 395X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 396X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 397X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 398X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 399X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 400X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 401X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 402X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 403X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 404X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 405X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 406X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 407X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 408X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 409X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 410X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 411X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 412X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 413X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 414X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 415X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 416X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 417X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 418X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 419X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 420X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 421X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 422X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 423X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 424X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 425X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 426X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 427X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 428X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 429X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 430X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 431X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 432X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 433X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 434X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 435X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 436X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 437X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 438X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 439X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 440X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 441X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 442X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 443X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 444X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 445X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 446X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 447X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 448X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 449X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 450X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 451X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 452X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 453X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 454X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 455X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 456X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 457X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 458X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 459X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 460X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 461X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 462X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 463X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 464X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 465X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 466X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 467X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 468X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 469X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 470X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 471X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 472X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 473X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 474X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 475X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 476X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 477X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 478X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 479X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 480X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 481X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 482X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 483X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 484X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 485X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 486X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 487X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 488X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 489X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 490X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 491X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 492X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 493X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 494X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 495X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 496X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 497X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 498X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 499X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 500X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 501X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 502X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 503X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 504X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 505X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 506X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 507X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 508X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 509X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 510X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 511X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 512X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 513X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 514X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 515X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 516X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 517X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 518X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 519X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 520X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 521X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 522X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 523X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 524X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 525X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 526X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 527X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 528X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 529X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 530X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 531X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 532X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 533X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 534X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 535X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 536X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 537X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 538X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 539X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 540X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 541X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 542X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 543X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 544X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 545X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 546X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 547X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 548X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 549X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 550X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 551X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 552X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 553X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 554X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 555X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 556X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 557X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 558X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 559X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 560X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 561X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 562X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 563X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 564X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 565X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 566X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 567X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 568X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 569X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 570X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 571X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 572X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 573X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 574X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 575X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 576X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 577X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 578X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 579X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 580X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 581X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 582X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 583X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 584X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 585X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 586X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 587X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 588X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 589X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 590X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 591X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 592X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 593X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 594X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 595X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 596X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 597X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 598X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 599X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 600X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 601X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 602X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 603X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 604X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 605X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 606X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 607X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 608X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 609X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 610X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 611X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 612X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 613X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 614X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 615X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 616X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 617X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 618X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 619X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 620X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 621X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 622X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 623X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 624X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 625X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 626X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 627X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 628X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 629X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 630X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 631X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 632X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 633X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 634X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 635X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 636X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 637X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 638X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 639X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 640X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 641X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 642X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 643X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 644X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 645X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 646X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 647X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 648X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 649X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 650X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 651X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 652X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 653X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 654X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 655X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 656X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 657X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 658X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 659X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 660X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 661X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 662X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 663X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 664X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 665X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 666X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 667X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 668X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 669X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 670X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 671X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 672X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 673X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 674X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 675X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 676X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 677X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 678X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 679X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 680X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 681X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 682X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 683X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 684X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 685X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 686X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 687X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 688X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 689X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 690X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 691X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 692X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 693X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 694X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 695X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 696X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 697X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 698X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 699X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 700X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 701X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 702X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 703X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 704X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 705X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 706X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 707X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 708X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 709X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 710X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 711X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 712X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 713X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 714X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 715X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 716X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 717X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 718X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 719X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 720X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 721X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 722X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 723X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 724X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 725X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 726X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 727X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 728X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 729X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 730X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 731X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 732X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 733X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 734X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 735X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 736X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 737X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 738X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 739X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 740X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 741X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 742X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 743X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 744X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 745X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 746X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 747X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 748X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 749X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 750X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 751X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 752X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 753X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 754X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 755X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 756X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 757X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 758X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 759X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 760X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 761X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 762X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 763X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 764X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 765X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 766X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 767X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 768X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 769X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 770X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 771X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 772X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 773X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 774X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 775X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 776X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 777X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 778X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 779X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 780X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 781X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 782X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 783X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 784X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 785X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 786X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 787X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 788X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 789X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 790X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 791X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 792X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 793X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 794X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 795X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 796X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 797X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 798X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 799X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 800X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 801X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 802X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 803X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 804X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 805X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 806X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 807X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 808X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 809X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 810X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 811X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 812X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 813X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 814X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 815X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 816X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 817X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 818X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 819X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 820X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 821X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 822X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 823X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 824X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 825X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 826X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 827X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 828X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 829X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 830X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 831X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 832X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 833X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 834X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 835X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 836X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 837X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 838X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 839X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 840X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 841X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 842X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 843X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 844X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 845X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 846X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 847X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 848X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 849X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 850X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 851X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 852X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 853X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 854X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 855X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 856X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 857X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 858X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 859X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 860X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 861X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 862X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 863X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 864X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 865X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 866X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 867X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 868X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 869X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 870X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 871X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 872X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 873X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 874X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 875X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 876X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 877X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 878X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 879X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 880X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 881X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 882X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 883X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 884X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 885X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 886X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 887X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 888X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 889X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 890X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 891X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 892X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 893X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 894X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 895X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 896X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 897X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 898X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 899X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 900X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 901X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 902X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 903X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 904X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 905X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 906X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 907X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 908X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 909X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 910X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 911X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 912X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 913X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 914X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 915X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 916X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 917X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 918X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 919X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 920X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 921X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 922X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 923X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 924X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 925X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 926X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 927X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 928X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 929X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 930X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 931X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 932X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 933X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 934X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 935X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 936X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 937X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 938X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 939X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 940X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 941X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 942X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 943X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 944X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 945X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 946X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 947X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 948X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 949X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 950X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 951X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 952X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 953X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 954X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 955X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 956X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 957X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 958X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 959X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 960X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 961X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 962X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 963X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 964X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 965X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 966X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 967X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 968X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 969X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 970X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 971X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 972X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 973X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 974X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 975X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 976X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 977X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 978X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 979X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 980X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 981X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 982X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 983X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 984X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 985X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 986X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 987X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 988X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 989X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 990X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 991X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 992X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 993X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 994X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 995X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 996X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 997X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 998X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 999X ᥇ꪖꪖ᥅ 😈💢",
    f"{target} ꪻꫀ᥅꠸ ꪑꪖꪖ ᥴꫝꪊᦔ꠸ 1000X ᥇ꪖꪖ᥅ 😈💢",
    ]

    global gcnc_active
    gcnc_active = True
    try:
        while gcnc_active:
            for template in templates:
                if not gcnc_active:
                    break
                try:
                    await ctx.channel.edit(name=template)
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 15
                        await asyncio.sleep(retry_after)
                    else:
                        raise e
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: Target NC loop stopped\n> __Error__: `{str(e)}`", delete_after=5)
    finally:
        gcnc_active = False

@bot.command()
async def stopgcnc(ctx):
    await ctx.message.delete()
    global gcnc_active, profilenc_active
    gcnc_active = False
    profilenc_active = False
    if ctx.channel.id in changing_gcs:
        changing_gcs[ctx.channel.id] = False
    await ctx.send("> **Stopped all rename loops.**", delete_after=5)

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


bot.run(token)

