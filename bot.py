import discord
from discord.ext import commands
import random

intents = discord.Intents.all()

settings = {
    'token': 'BOT_TOKEN',
    'bot': 'AqoBot',
    'id': 807855669880815646,
    'prefix': '!'
}

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

bot.remove_command('help')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
    emb = discord.Embed(title="Информация о боте:")

    emb.add_field(name='О боте:', value="В боте присутсвует фильтр чата, если вы употребляете ненормативную лексику или же оскорбляете кого-то, то бот выдаст роль мута. Присутсвуют логи удаленных сообщений")
    emb.add_field(name='{}ban'.format(settings['prefix']), value="Банит участника")
    emb.add_field(name='{}tag'.format(settings['prefix']), value="Выдает случайному участнику сервера задачу. Пример: !tag работа")
    emb.add_field(name='Примечание:', value="Для корректной работы бота вам нужно иметь чаты с названием: Правила, Информация, logs, общение(чат с общением участников), а также роль с названием: mute. Канал с названием logs должен быть доступен только модерации сервера, роль mute должна запрещать писать сообщения в чатах")

    await ctx.send(embed = emb)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'Был забанен.{member.mention}')


delete_words = []
file = open("Список.txt", "r", encoding="utf-8")
delete_words = file.read().strip().split(", ")

file.close()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    else:
        content = message.content
        for word in content.split():
            for bad_word in delete_words:
                if bad_word.lower() in word.lower():
                    c1 = discord.utils.get(message.guild.channels, name="правила")
                    await message.delete()
                    await message.channel.send(f"Данные слова запрещены правилами! Прочитайте {c1.mention}.")
                    roles = discord.utils.get(message.guild.roles, name='mute')
                    await message.author.add_roles(roles)



@bot.event
async def on_member_join(member: discord.Member):

    channel = discord.utils.get(member.guild.channels, name="общение")
    c1 = discord.utils.get(member.guild.channels, name="правила")
    c2 = discord.utils.get(member.guild.channels, name="информация")
    await channel.send(f'Привет, {member.mention}! Прочитай {c1.mention} и {c2.mention}.')


@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="{} удалил сообщение".format(message.author.name),
                          description="", colour=200)
    embed.add_field(name=message.content, value="Это сообщение было удалено",
                    inline=True)
    channel = discord.utils.get(message.guild.channels, name="logs")
    await channel.send(channel, embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def tag(ctx):
    user = random.choice(ctx.message.channel.guild.members)
    author = ctx.message.author
    role_name = ctx.message.content.replace(ctx.message.content.split(" ")[0] + " ", "")
    user1 = ctx.message.author

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        pass
    else:
        await ctx.guild.create_role(name=role_name)
        role = discord.utils.get(ctx.guild.roles, name=role_name)

    await user.add_roles(role)
    embed = discord.Embed(title=f"⚒ Выдаёт работу \"{role_name}\" ", colour=discord.Colour(0x9faa7f),
                          description=f"👥 пользователю <@{user.id}>")

    embed.set_author(name=f"{author}", icon_url=author.avatar_url)

    await ctx.send(embed=embed)

bot.run(settings['token'])
