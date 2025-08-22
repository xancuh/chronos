import discord
from discord.ext import commands
import secrets
import string

# This is V1 for the bot. It is very vulnerable and has loads of bugs. Do NOT use this for your server

# --------------- CONFIG ---------------- #
TOKEN = "enter bot token here"
PREFIX = "!" # you can use any prefix. /, ?, & etc. make sure it is a symbol
LOG_CHANNEL_ID = enter log channel id here
# ------------- CONFIG END -------------- #

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # needed for guild member lookup
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

issued_keys = {}

def generate_key():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    random_part = ''.join(secrets.choice(alphabet) for _ in range(16)) # you can set 16 to how much characters you want in your keys (8 for example

    return f"chronos-{random_part}"

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}. The bot is online and ready for use!")

@bot.command(name="idchecker")
async def idchecker(ctx, user_id: int = None):
    if user_id is None:
        await ctx.send("Error 10: Please provide a user ID. Usage: `!idchecker <userId>`")
        return

    try:
        user = await bot.fetch_user(user_id)

        embed = discord.Embed(title="User Information", color=0x3498db)
        embed.add_field(name="Username", value=user.name, inline=True)
        if hasattr(user, "discriminator"):
            embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Mention", value=user.mention, inline=False)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

        await ctx.send(embed=embed)

    except discord.NotFound:
        await ctx.send("No user found with that ID.")
    except discord.HTTPException:
        await ctx.send("Error 400: Make your profile public, or try again.")

@bot.command(name="createkey")
async def create_key(ctx, username: str = None):
    if ctx.guild is None:
        await ctx.send("This command can only be used inside a server. Please join or go to the Chronos server and try again.")
        return

    if username is None:
        await ctx.send("Please provide a Discord username. Usage: `!createkey <username>`")
        return

    
    member = discord.utils.find(lambda m: m.name == username or str(m) == username, ctx.guild.members)
    if member is None:
        await ctx.send("That username is not in this server. Make sure you type it exactly as it appears.")
        return

    
    if member.id in issued_keys:
        await ctx.send(f"{member.mention} already has a key issued. Their key has been sent via DMs.")
        return

    
    key = generate_key()
    issued_keys[member.id] = key

    try:
        embed = discord.Embed(title="Invite Key:", description="Here is your unique key:", color=0x2ecc71) # change title and description if needed
        embed.add_field(name="Key", value=f"`{key}`", inline=False)
        embed.set_footer(text="Keep this key safe and private. It will expire after your application is sent.") # change text if needed
        await member.send(embed=embed)
        await ctx.send(f"Key has been sent privately to {member.mention}!")
    except discord.Forbidden:
        await ctx.send(f"The DM to {member.mention} has not been sent. They might have DMs disabled.")
        return

    
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f"**Key Generated!** | User: `{member}` | (Key sent privately)")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error 403: Try re-entering the code.")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send("Error 909: The bot may be offline, or there was an attack. Contact @username immediately.")
        raise error

bot.run(TOKEN)
