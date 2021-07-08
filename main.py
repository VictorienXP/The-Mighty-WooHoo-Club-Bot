import json
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import webcolors

with open('config.json') as config_file:
    config = json.load(config_file)

guild_id = config['guild_id']
guild_ids = [guild_id]
owner_id = config['owner_id']
role_position = config['role_position']
roles_with_color_access = config['roles_with_color_access']

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def change_color(guild, member, color):
    colorRole = discord.utils.find(lambda r: r.name == str(member.id), guild.roles)
    try:
        color = webcolors.name_to_hex(color)
        print('Interpreted as {0}.'.format(color))
    except:
        pass
    try:
        color = int(color.replace("#", ""), 16)
        if color > 16777215:
            print('The input is too huge.')
            return "<:YAMERO:465570543781937172> Your input is too huge!"
    except ValueError:
        print('The input is invalid.')
        return "❌ I am unable to understand your input! I only understand hexadecimal/HTML/CSS3 color codes/names."
    except:
        print('Something gone wrong.')
        return "<:DAT_FACE:442089694763810817> Oh no something broke!"
    if not colorRole:
        colorRole = await guild.create_role(name=member.id, colour=discord.Colour(color))
        positron = discord.utils.find(lambda r: r.id == role_position, guild.roles)
        await colorRole.edit(position=positron.position - 1)
        await member.add_roles(colorRole)
        print('{0} has been created for {1}'.format(colorRole, member))
        return 0
    elif not colorRole in member.roles:
        await member.add_roles(colorRole)
    try:
        await colorRole.edit(colour=discord.Colour(color))
    except discord.errors.Forbidden:
        print('Forbidden.')
        return "<a:ThisIsFineIntensifies:442094172682452993> I don't have access to the role!"
    except:
        print('Something gone wrong.')
        return "<:DAT_FACE:442089694763810817> Oh no something broke!"
    print('{0} has been updated for {1}'.format(colorRole, member))
    return 0

@slash.slash(name="changecolor",
            description="Change your color",
            guild_ids=guild_ids,
            options=[
                create_option(
                    name="color",
                    description="The color you want in hex format",
                    option_type=3,
                    required=True,
                )
            ])
async def _changecolor(ctx, color: str):
    print('{0.author} requested a color change to {1}'.format(ctx, color))
    if not discord.utils.find(lambda r: r.name == str(ctx.author.id), ctx.author.roles) and not discord.utils.find(lambda r: any(r.id == id for id in roles_with_color_access), ctx.author.roles):
        await ctx.send(content="🚫 You are not allowed to choose a color.\nIn order to choose a color you need any of these roles: " + ", ".join("<@&{}>".format(id) for id in roles_with_color_access), hidden=True)
        print('But they are not allowed.')
        return
    result = await change_color(ctx.guild, ctx.author, color)
    if result:
        await ctx.send(content=result, hidden=True)
    else:
        await ctx.send(content="✅ Your color has been updated!", hidden=True)

@slash.slash(name="ping", description="go for the pong", guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(content=f"Pong! ({client.latency*1000:.4f}ms)", hidden=True)

@slash.slash(name="shutdown", description="Shutdown the bot", guild_ids=guild_ids)
async def _exit(ctx):
    if ctx.author_id == owner_id:
        await ctx.send(content="ok I go poof", hidden=True)
        await client.close()
    else:
        await ctx.send(content="no u", hidden=True)

client.run(config['token'])
