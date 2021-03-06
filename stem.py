import discord
import os
import asyncio
import datetime
from discord.ext import commands
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import Bot
import sys
import random

from config import settings
import configg

nd = datetime.datetime.now()

client = commands.Bot(command_prefix = settings["PREFIX"], intents=discord.Intents(
        guilds=True, members=True, messages=True, reactions=True, presences=True, voice_states=True
    ))
client.remove_command( 'help' )
#-------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
	now_time = nd.strftime("%H:%M:%S") 
	print(">> Консоль <<" " Бот запущен "+(now_time)) 
	await client.change_presence( status = discord.Status.online, activity=discord.Game ("Discord") )
	#printer.start()

#@tasks.loop(minutes=12)
#async def printer():
	#channel = client.get_channel(848248409806602301)
	#nds = datetime.datetime.now()
	#now_time = nds.strftime(" %H:%M:%S ")
	#await channel.send(f"Привет!")

@client.event
async def on_member_join(member):
	channel = client.get_channel(825463627586601000)

	emb = discord.Embed(title = 'ДОБРО ПОЖАЛОВАТЬ', description = f'**{member.name}** приветствуем тебя на сервере {member.guild.name}. На нашем сервере мы проводим ивенты, общаемся и играем в разные игры.\n\n**ОЗНАКОМЬСЯ С ДАННЫМИ КАНАЛАМИ:**\n:arrow_forward: <#825464795784151111>\nОзнакомься с правилами сервера.\n:arrow_forward: <#825466544141238303>\nсписок команд для взаимодействия с ботами.\n:arrow_forward: <#825694586441695262>\nпроходят ежедневные розыгрыши с хорошими призами.', color = 0xCC974F)
	emb.set_footer(text="ПРИЯТНОГО ВРЕМЯ ПРОВЕДЕНИЯ НА НАШЕМ СЕРВЕРЕ")

	role_1 = member.guild.get_role(838788077547028571)
	await member.add_roles(role_1)
	beta = member.guild.get_role(825854167767711745)
	await member.add_roles(beta)
	lvl = member.guild.get_role(846281368547360779)
	await member.add_roles(lvl)
	
	await channel.send(embed = emb)

Bad_word = ["бан","кик"] 

@client.event 
async def on_message(message): 
	await client.process_commands(message) 
	mes = message.content.lower()
	avtorMsg = message.author.name 
	channelMassage = message.channel.id
	channelMassage2 = message.channel.name
	now_datetime = datetime.datetime.now() 
	now_times = nd.strftime(" = %H : %M : %S = ") 
	date_dm = nd.strftime(" - %d.%m.%y %b -") 
	print(format(now_datetime) + " > " + str(channelMassage) + "-" + channelMassage2 + " > " + avtorMsg + " > " + mes) 
	with open("Massage.txt", "a", encoding = "utf-8") as logmsg: 
		logmsg.write(f"{date_dm} >>> {now_times} >> {channelMassage}-{channelMassage2} > {avtorMsg} = {mes}\n") 

@client.event
async def on_voice_state_update(member, before, after):
	if after.channel.id == 825730949249630218:
		for guild in client.guilds:
			maincategory = discord.utils.get(guild.categories, id=825730948715905076)
			channel2 = await guild.create_voice_channel(name=f'Канал {member.display_name}', category = maincategory)
			print(f'Канал {channel2} создан!')
			await channel2.set_permissions(member,connect=True,manage_channels=True)
			await member.move_to(channel2)
			def check(x,y,z):
				return len(channel2.members) == 0
			await client.wait_for('voice_state_update',check=check)
			await channel2.delete()
			print(f'Канал {channel2} удален!')

@client.event
async def on_raw_reaction_add(payload):
        if payload.message_id == configg.POST_ID:
            channel = client.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = get(message.guild.roles, id=configg.ROLES[emoji]) # объект выбранной роли (если есть)
            
                if(len([i for i in member.roles if i.id not in configg.EXCROLES]) <= configg.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
		
@client.event
async def on_raw_reaction_remove(payload):
        channel = client.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = get(message.guild.roles, id=configg.ROLES[emoji]) # объект выбранной роли (если есть)
 
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

		
#-------------------------------------------------------------------------------------------------
@client.command(aliases = ["clear","очистка", "cl"])
@commands.cooldown(1, 8, commands.BucketType.user)
@commands.has_any_role("модератор", "администратор")
async def __clear(ctx, amount = 1):
	await ctx.channel.purge(limit = 1)
	await asyncio.sleep(1)
	await ctx.channel.purge(limit = amount)
	Mas = await ctx.send(f':thumbsup: Удалено {amount} сообщений')
	await asyncio.sleep(4)
	await Mas.delete()

@client.command(aliases = ["reload", "перезагрузка"])
@commands.has_any_role("администратор", ".")
async def __reload(ctx):
	embed = discord.Embed(description = "**БОТ ПЕРЕЗАПУСКАЕТСЯ**", color = 0xf5ce42)
	embedmas = await ctx.send(embed=embed)
	await asyncio.sleep(2)
	await embedmas.delete()
	await os.execv(sys.executable, ["python"] + sys.argv)
	
@client.command(aliases = ["mute", "мут"])
@commands.has_permissions(view_audit_log=True)
async def __mute(ctx,member:discord.Member,time=0,*,reason=None):
	if reason == None:
		return await ctx.send("Ошибка\n`.mute [name] [time] [reason]`")
	
	if member.top_role >= ctx.author.top_role:
		return await ctx.send(f'Ты не можешь **muted** модератора!')
		
	if member.id == ctx.author.id:
		return await ctx.send(f"{ctx.author.mention}, ты не можешь **muted** себя!")
	
	mults = {"m": 60, "h": 60 * 60, "d": 60 * 60 * 24}
	try:
		seconds = int(time)
	except ValueError:
		seconds = (time[:-1]) * mults.get(time[-1], 1)

	muterole = discord.utils.get(ctx.guild.roles, id=825804010271145984)
	emb = discord.Embed(title=f'ВЫ ПОЛУЧИЛИ МЬЮТ НА int{time} секунд ПО ПРИЧИНЕ {reason}', color = 0xf5ce42)
	await member.add_roles(muterole)
	await member.send(embed=emb)
	await ctx.send(f":white_check_mark: Пользователь **muted** успешно")
	await asyncio.sleep(time)
	await member.remove_roles(muterole)

@client.command()
@commands.has_any_role("администратор", ".")
async def unmute(ctx,member:discord.Member):
	muterole = discord.utils.get(ctx.guild.roles, id=825804010271145984)
	print(f'Пользователь {member} успешно размьючен')
	await ctx.send(f":white_check_mark: Пользователь **unmuted** успешно")
	await member.remove_roles(muterole)

@client.command(aliases = ["ban", "бан"])
@commands.has_any_role("администратор", ".")
async def __ban(ctx,member:discord.Member):
	if member.id == ctx.author.id:
		return await ctx.send(f"{ctx.author.mention}, ты не можешь **banned** себя!")

	await ctx.send(f":white_check_mark: Пользователь **banned** успешно")
	print(f'Пользователь {member} упешно забанен')
	await member.ban()

#-------------------------------------------------------------------------------------------------
@client.command(aliases = ["ping","пинг"])
@commands.cooldown(1, 6, commands.BucketType.user)
async def __ping(ctx):
	await ctx.send(f'Ping: {round(client.latency * 1000)}ms')


	
token = os.environ.get('token')
client.run(token)
