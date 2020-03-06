import discord
from discord.ext import commands
from discord.utils import get
from discord.utils import get
import youtube_dl, os


PREFIX = '.'
bad_words = [ 'кик', 'бан', 'сука', 'блять', 'пидор', 'дима пидор', 'все пидорасы', 'шлюха', 'говно' ]


client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )


@client.event

async def on_ready():
    print('Bot Connected')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence( status = discord.Status.online, activity = discord.Game( '.help' ) )



    
@client.event
async def  on_command_error( ctx, error ):
    pass 

# тест
@client.event

async def on_member_join( member ):
    channel = client.get_channel(656831104061276160  )

    role = discord.utils.get( member.guild.roles, id = 656876657407164419  )   

    await member.add_roles( role )
    await channel.send( embed= discord.Embed( description = f'Пользователь { member.name }, присоединился кнам! ') )



# Filter
@client.event
async def on_message( message ):
    await client.process_commands( message )

    msg = message.content.lower()

    if msg in bad_words:
        await message.delete()
        await message.author.send( f'{ message.author.name }, не надо такое писать!')

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Пожалуйста ожидайте')

    voice = get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывает музыка: {song_name[0]}')



@client.command( pass_context = True )
async def hello( ctx ):
    author = ctx.message.author
    
    await ctx.send( f' { author.mention } Hello. Я бот дискорда' )


# Clear message
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )  

async def clear( ctx, amount : int ):
    await ctx.channel.purge( limit = amount )

# Clear commmand

# kick
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge(limit = 1 )

    await member.kick( reason = reason )
    await ctx.send( f'kick user { member.mantion }' )


# ban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban(ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.ban( reason = reason )
    await ctx.send( f'ban user { member.mention } ' )


# unban
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban ( user )
        await ctx.send( f'Unbanned user { user.mention }' )

        return


#comand help
@client.command( pass_context = True )
async def help( ctx ):
    embed = discord.Embed(title="Список команд бота", description="", color=0xeee657)


    embed.add_field(name=".hello", value="Привтсвие от бота", inline=False)
    embed.add_field(name=".send_m", value="Передать привет пользователю", inline=False)
    embed.add_field(name=".info", value="Информацыя о боте", inline=False)
    embed.add_field(name=".clear", value="Очистка чата", inline=False)
    embed.add_field(name=".mute", value="Мут пользователя в тектовых и глосовых каналах", inline=False)
    embed.add_field(name=".kick", value="Выгоняет пользователя", inline=False)
    embed.add_field(name=".ban", value="Блокирует доступ к серверу", inline=False)
    embed.add_field(name=".unban", value="Разбанивает игрока", inline=False)

    await ctx.send(embed=embed) 






        #command info
@client.command( pass_context = True )
async def info( ctx ):
      embed = discord.Embed(title="Привет", description="Информацыия по боту.", color=0xeee657)

       # give info about you here
      embed.add_field(name="developer", value="[<Dmitry Popovych>](<https://discordapp.com/channels/@me/685540246699376711>)")
    
    # Shows the number of servers the bot is member of.
      embed.add_field(name="servers", value=f"{len(client.guilds)}")

    # give users a link to invite thsi bot to their server
      embed.add_field(name="invite", value="[Сылка на приглашенния бота](<https://discordapp.com/oauth2/authorize?client_id=653265199662366720&scope=bot&permissions=8>)")

      await ctx.send(embed=embed)

# Mute

@client.command( pass_context = True )
@commands.has_permissions( administrator = True )
async def mute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )

    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute')
                                   
    await member.add_roles( mute_role)
    await ctx.send( f'y { member.mention }, Ограниченние чата и голосових каналов, за нарушенние правил !' )

# private messge
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def send_a( ctx ):
    await ctx.author.send ( 'Hello Word!' )

@client.command( pass_context = True )
async def send_m( ctx, member: discord.Member ):
    await member.send( f'{ member.name }, привет от { ctx.author.name } ' )


@client.command( pass_context = True )
@commands.has_permissions( administrator = True )
async def send_mp( ctx, member: discord.Member ):    
    await member.send( f'{ member.name },Пошел нахуй. Ето пранк аахахах ' )


@client.command( pass_context = True )
async def send_1( ctx, member: discord.Member ):    
    await member.send( f'{ member.name },Добав мення вот сылочка  https://discordapp.com/oauth2/authorize?client_id=653265199662366720&scope=bot&permissions=8 ' )




@clear.error
async def clear_error( ctx, error ):
    if isinstance( error,  commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажыте аргумент ' )

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав! ' )


@mute.error
async def mute_error( ctx, error ):
    if isinstance( error,  commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажыте аргумент ' )

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав! ' )


@kick.error
async def kick_error( ctx, error ):
    if isinstance( error,  commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажыте аргумент ' )

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав! ' )


@ban.error
async def ban_error( ctx, error ):
    if isinstance( error,  commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажыте аргумент ' )

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав! ' )


@unban.error
async def unban_error( ctx, error ):
    if isinstance( error,  commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажыте аргумент ' )

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send( f'{ ctx.author.name }, у вас недостаточно прав! ' )

@send_m.error
async def send_m_error( ctx, error ):
    if isinstance( error,  commands.MissingRequiredArgument ):
        await ctx.send( f'{ ctx.author.name }, обязательно укажыте аргумент ' )



@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f' Бот присоединился к каналу: {channel}') 



@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.disconnect() 
        await ctx.send(f' Бот отключился от канала: {channel}')




'''@
async def CommandNotFound_error( ctx, error ):
    if isinstance( error, commands.CommandNotFound ):
        await ctx.send( f'{ctx.author.name }, Нет такой команды! ' )'''



 




# Connect
token = open( 'token.txt', 'r' ).readline()

client.run( token )


