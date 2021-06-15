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

	emb = discord.Embed(title = 'ДОБРО ПОЖАЛОВАТЬ', description = f'**{member.name}** приветствуем тебя на сервере {member.guild.name}. На нашем сервере мы проводим ивенты, общаемся и играем в разные игры.\n\n**ОЗНАКОМЬСЯ С ДАННЫМИ КАНАЛАМИ:**', color = 0xCC974F)
	emb.add_field(
        name = '<#825464795784151111>',
        value = 'Ознакомься с правилами сервера.', inline = False)
	emb.add_field(
        name = '<#825466544141238303>',
        value = 'список команд для взаимодействия с ботами.', inline = False)
	emb.add_field(
        name = '<#825694586441695262>',
        value = 'проходят ежедневные розыгрыши с хорошими призами.', inline = False)
	emb.set_footer(text="ПРИЯТНОГО ВРЕМЯ ПРОВЕДЕНИЯ НА НАШЕМ СЕРВЕРЕ")

	role_1 = member.guild.get_role(838788077547028571)
	await member.add_roles(role_1)
	beta = member.guild.get_role(825854167767711745)
	await member.add_roles(beta)
	lvl = member.guild.get_role(846281368547360779)
	await member.add_roles(lvl)
	
	await channel.send(embed = emb)

Bad_word = ["010101"] 

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
	for i in Bad_word: 
		if i in mes:
			await message.delete()
			msg = await message.channel.send(f"Не надо такие страсти говорить")
			with open("Bad.txt", "a", encoding = "utf-8") as logmsg:
				logmsg.write(f"{date_dm} >>> {now_times} >> {channelMassage}-{channelMassage2} > {avtorMsg} = {mes}\n")
			await asyncio.sleep(8)
			await msg.delete()

@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        Err1 = await ctx.send(embed=discord.Embed(description=f"Команда не найдена!"))
        await asyncio.sleep(6)
        await Err1.delete()

    elif isinstance(err, commands.BotMissingPermissions):
        Err2 = await ctx.send(
            embed=discord.Embed(description=f"У бота отсутствуют права: {' '.join(err.missing_perms)}\nВыдайте их ему для полного функционирования бота"))
        await asyncio.sleep(6)
        await Err2.delete()

    elif isinstance(err, commands.MissingPermissions):
        Err3 = await ctx.send(embed=discord.Embed(description=f"У вас недостаточно прав для запуска этой команды!"))
        await asyncio.sleep(6)
        await Err3.delete()

    elif isinstance(err, commands.CommandOnCooldown):
        Err5 = await ctx.send(embed=discord.Embed(description=f"У вас еще не прошел кулдаун на команду {ctx.command}!\nПодождите еще {err.retry_after:.2f}"))
        await asyncio.sleep(6)
        await Err5.delete()

    elif isinstance(err, dpy_errors.Forbidden):
        Err6 = await ctx.send(embed=discord.Embed(description=f"У бота нет прав на запуск этой команды!"))
        await asyncio.sleep(6)
        await Err6.delete()
	
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

#-------------------------------------------------------------------------------------------------
#@client.command(aliases = ["лог", "log"])
#@commands.cooldown(1, 24, commands.BucketType.user)
#@commands.has_any_role("админ")
#async def log(ctx):
	#Masg = await ctx.send(file = discord.File(fp = "Massage.txt"))
	#await asyncio.sleep(12)
	#await Masg.delete()

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
async def __mute(ctx,member:discord.Member,*,time:int,reason):
	muterole = discord.utils.get(ctx.guild.roles, id=825804010271145984)
	emb = discord.Embed(title=f'ВЫ ПОЛУЧИЛИ МЬЮТ НА' + time + 'ПО ПРИЧИНЕ' + reason, color = 0xf5ce42)
	await member.add_roles(muterole)
	await member.send(embed=emb)
	#print(f'Пользователь {member.mention} получил мьют на {time} по причине {reason} модератором {ctx.message.author.mention}')
	await ctx.send(f":white_check_mark: Пользователь **muted** пользователя")
	await asyncio.sleep(time)
	await member.remove_roles(muterole)
	


@client.command(aliases = ["ban", "бан"])
@commands.has_any_role("администратор", ".")
async def __ban(ctx):
	pass
	
#-------------------------------------------------------------------------------------------------
@client.command(aliases = ["ping","пинг"])
@commands.cooldown(1, 6, commands.BucketType.user)
async def __ping(ctx):
	await ctx.send(f"понг!")
	
	
	
	

token = os.environ.get('token')
client.run(token)
