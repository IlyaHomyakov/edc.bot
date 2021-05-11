from __future__ import unicode_literals
from datetime import datetime
import random
import discord
import requests
import math
from discord.ext import commands


client = discord.Client

TOKEN = ''
bot = commands.Bot(command_prefix='!', help_command=None)


@bot.command()
async def h(ctx):
    await help.invoke(ctx)
    await ctx.message.delete()


@bot.command()
async def help(ctx):
    changelog_file = open('helpcommands.txt', 'r', encoding="utf-8")
    await ctx.send('```' + changelog_file.read() + '```')
    await ctx.message.delete()


@bot.command()
async def pa(ctx, *, args):  # создаем асинхронную фунцию бота
    await ctx.send('```' + args + ', приятного аппетита!```')
    await ctx.message.delete()


@bot.command()  # разрешаем передавать агрументы
async def roll(ctx, *args):  # создаем асинхронную фунцию бота
    print('аргументов передано: ' + str(len(args)))
    if len(args) > 1:
        await ctx.send('```Слишком много аргументов! Используйте !roll *число*```')
    elif len(args) == 1:
        roll_num = args[0]
        print(roll_num)
        try:
            roll_num = float(roll_num)
            if math.modf(roll_num)[0] == 0:
                roll_num = int(math.modf(roll_num)[1])
            if roll_num > 0:
                await ctx.send("```Выбираю случайное число от 0 до " + str(roll_num) + ": " + str(
                    random.randrange(0, roll_num, 1)) + '```')  # отправляем обратно аргумент
            if roll_num < 0:
                await ctx.send("```Выбираю случайное число от " + str(roll_num) + " до 0: " + str(
                    random.randrange(int(roll_num), 0, 1)) + '```')  # отправляем обратно аргумент
            if int(roll_num) == 0:
                await ctx.send('```Держи 0, умник!```')
        except:
            await ctx.send('```Аргумент должен быть целым числом!```')

    else:
        await ctx.send(
            "```Выбираю случайное число: " + str(random.randint(0, 1000000)) + '```')  # отправляем обратно аргумент
    await ctx.message.delete()


@bot.command()  # разрешаем передавать агрументы
async def ask(ctx, *, args):  # создаем асинхронную фунцию бота
    answers_array = ['Думаю, да!', 'Думаю, нет', 'Нет', 'Да', 'Спроси позже', 'Не хочу говорить', 'Бесспорно',
                     'Даже не думай!', 'Сконцентрируйся и спроси опять', 'Можешь быть уверен в этом',
                     'Лучше не рассказывать', 'Сейчас нельзя предсказать', 'Перспективы не очень хорошие',
                     'Весьма сомнительно', 'Хорошие перспективы', 'Предрешено', 'Никаких сомнений', 'Не ебу',
                     'Тебе виднее', 'Такое я не могу знать', 'Может это знает кто-нибудь из edc?']
    answer = random.choice(answers_array)
    author_nick = ctx.author.nick
    if author_nick is None:
        author_nick = ctx.author.name
    await ctx.send('```' + author_nick + ' спрашивает: «' + args + '» — ' + answer + '```')
    await ctx.message.delete()


@bot.command()
async def say(ctx, *, args):
    await ctx.send('```' + args + '```')
    await ctx.message.delete()


@bot.command()
async def flip(ctx):
    coin_side_arr = ['Орел', 'Решка']
    coin_side = random.choice(coin_side_arr)
    await ctx.send('```А как мы их поделим? Подбрось монетку, флип...\n'
                   'И выпадает... ' + coin_side + '!```')
    await ctx.message.delete()


@bot.command()
async def weather(ctx, *, args):
    city_name = args
    api_key = 'c3f875ecca22e600a385a36293ce4d4c'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&lang=ru&units=metric&appid=' + api_key
    weather_response = requests.get(url)
    response_code = weather_response.json()['cod']
    if response_code == '404':
        await ctx.send('```Эта территория еще неизведана!```')
    else:
        main_data = weather_response.json()['main']
        sys_data = weather_response.json()['sys']

        weather_description = weather_response.json()['weather'][0]['description']  # ясно/туманно и т.п.
        temp = main_data['temp']  # температура сейчас
        min_temp = main_data['temp_min']  # минимальная температура
        max_temp = main_data['temp_max']  # максимальная температура
        humidity = main_data['humidity']  # влажность
        feels_like_temp = main_data['feels_like']  # ощущается

        country = sys_data['country']  # название страны: BY, US и ид
        sunset_time = sys_data['sunset']  # время захода
        sunrise_time = sys_data['sunrise']  # время восхода

        name = weather_response.json()['name']  # название города
        request_date = weather_response.json()['dt']  # дата запроса
        pressure_mm_rt_st = 0.75 * int(main_data['pressure'])  # давление в мм рт ст

        weather_output = ('```{}, {}, {}:\n'
                          'Сейчас {}°C, ощущается как {}°C, минимальная температура {}°C, максимальная {}°C, {}.\n'
                          'Влажность {}%, давление {} мм.рт.ст.\n'
                          'Восход в {}, заход в {} (время РБ)```').format(
            name, country, datetime.fromtimestamp(request_date).strftime('%d-%m-%Y %H:%M:%S'), temp,
            feels_like_temp, min_temp, max_temp, weather_description, humidity, pressure_mm_rt_st,
            datetime.fromtimestamp(sunrise_time).strftime('%H:%M:%S'),
            datetime.fromtimestamp(sunset_time).strftime('%H:%M:%S'))

        await ctx.send(weather_output)
        await ctx.message.delete()


@bot.command()
async def table(ctx, *args):
    prepared_string = ''
    group_num = args[0]
    response = requests.get('https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup=' + group_num)
    edu_week = requests.get('http://journal.bsuir.by/api/v1/week').json()
    if response.text == '':
        await ctx.send('```Такой группы нет```')

    today = datetime.today().weekday()

    if 0 <= datetime.now().hour < 2:  # проверяем на вызов в два ночи
        is_today = 'сегодня'
    else:  # если вызываем днем, выводим на следующий день
        today += 1
        is_today = 'завтра'

    if today >= 6:
        is_today = 'завтра'
        if today == 6:
            prepared_string += 'Завтра воскресенье. '
            is_today = 'понедельник'
        prepared_string += ''
        today = 0
        edu_week += 1
        if edu_week > 4:
            edu_week = 1

    schedules = response.json()['schedules']
    number_of_lessons = len(schedules[today]['schedule'])
    speciality = schedules[today]['schedule'][0]['studentGroupInformation'][0]
    prepared_string += ('Ищу расписание для группы ' + group_num + ' на ' + is_today + ', учебная неделя №' +
                        str(edu_week) + '\n')
    prepared_string += speciality + '\n\n'

    for i in range(number_of_lessons):
        if edu_week in schedules[today]['schedule'][i]['weekNumber']:

            if schedules[today]['schedule'][i]['numSubgroup'] == 0:
                sub_group = ''
            else:
                sub_group = '(подгр. ' + str(schedules[today]['schedule'][i]['numSubgroup']) + ')'

            if not schedules[today]['schedule'][i]['auditory']:
                auditory = ''
            else:
                auditory = schedules[today]['schedule'][i]['auditory'][0]

            subject = schedules[today]['schedule'][i]['subject']
            lesson_type = schedules[today]['schedule'][i]['lessonType']
            lesson_time = schedules[today]['schedule'][i]['lessonTime']

            prepared_string += (lesson_time + '  ' + subject + ':' + lesson_type + '  ' + auditory + '  '
                                + sub_group + '\n')

    await ctx.send('```' + prepared_string + '```')
    await ctx.message.delete()


@bot.command()
async def pic(ctx, *args):
    rqst = requests.get('https://picsum.photos/512/512')
    pic_url = rqst.url
    pic_file = requests.get(pic_url)
    open('random_pic.png', 'wb').write(pic_file.content)
    await ctx.send(file=discord.File('random_pic.png'))
    await ctx.message.delete()


@bot.command()
async def t(ctx):
    await ctx.send('```Это правда```')
    await ctx.message.delete()


@bot.command()
async def f(ctx, *args):
    await ctx.send('```Это неправда```')
    await ctx.message.delete()


@bot.event
async def on_ready():  # по умолчанию при запуске ставит статус на Слушает !help
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))
    print('Bot started successfully!')


@bot.command()
async def newrole(ctx, *, role_name):
    guild = ctx.guild
    author_nick = ctx.author.nick
    if author_nick is None:
        author_nick = ctx.author.name

    if role_name in [str(r.name) for r in guild.roles]:
        await ctx.send('```Роль «' + role_name + '» уже существует, можете вступить в нее, !join "роль"```')
    else:
        await guild.create_role(name=role_name)
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.message.author.add_roles(role)
        await ctx.send('```' + author_nick + ' создал роль «' + role_name + '» и вступил в нее, '
                       'присоединиться к ней можно при помощи команды !join ' + role_name + '```')
    await ctx.message.delete()


@bot.command()
async def join(ctx, *, role_name):
    guild = ctx.guild
    author_nick = ctx.author.nick
    if author_nick is None:
        author_nick = ctx.author.name
    try:
        if role_name not in [str(r.name) for r in guild.roles]:
            await ctx.send('```Роли «' + role_name + '» нет :(```')
        elif role_name in [str(r.name) for r in ctx.message.author.roles]:
            await ctx.send('```' + author_nick + ', вы уже состоите в роли «' + role_name + '»```')
        else:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await ctx.message.author.add_roles(role)
            await ctx.send('```' + author_nick + ', вы успешно вступили в роль «' + role_name +
                           '», чтобы выйти из нее, пропишите !leave ' + role_name + '```')
    except discord.errors.Forbidden:
        await ctx.send('```' + author_nick + ', вы не можете вступить в роль «' + role_name + '» :(```')
    await ctx.message.delete()


@bot.command()
async def leave(ctx, *, role_name):
    guild = ctx.guild
    author_nick = ctx.author.nick
    if author_nick is None:
        author_nick = ctx.author.name
    try:
        if role_name not in [str(r.name) for r in guild.roles]:
            await ctx.send('```Роли «' + role_name + '» нет, ее можно создать!```')
        elif role_name not in [str(r.name) for r in ctx.message.author.roles]:
            await ctx.send('```' + author_nick + ', вы не состоите в роли «' + role_name + '»```')
        else:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await ctx.message.author.remove_roles(role)
            await ctx.send('```' + author_nick + ', вы успешно покинули роль «' + role_name + '»```')
    except discord.errors.Forbidden:
        await ctx.send('```' + author_nick + ', вы не можете покинуть роль «' + role_name +
                       '». Вероятно, у вас недостаточно прав :(```')
    await ctx.message.delete()


@bot.command()
async def go(ctx, *, role_name):
    guild = ctx.guild
    author_nick = ctx.author.nick
    if author_nick is None:
        author_nick = ctx.author.name
    try:
        if role_name not in [str(r.name) for r in guild.roles]:
            await ctx.send('```Роли «' + role_name + '» на сервере нет.```')
        elif role_name not in [str(r.name) for r in ctx.message.author.roles]:
            await ctx.send('```' + author_nick + ', вы не состоите в роли «' + role_name +
                           '» и не можете собирать ее участников!```')
        else:
            moderator = discord.utils.get(ctx.guild.roles, name=role_name)
            await ctx.send(ctx.author.mention + ' собирает участников ' + moderator.mention)
    except discord.errors.Forbidden:
        await ctx.send('```' + author_nick + ', вы не можете собрать '
                       'участников роли «' + role_name + '». Вероятно, у вас недостаточно прав :(```')
    await ctx.message.delete()


@bot.command()
async def delrole(ctx, *, role_name):
    guild = ctx.guild
    author_nick = ctx.author.nick
    if author_nick is None:
        author_nick = ctx.author.name
    if role_name not in [str(r.name) for r in guild.roles]:
        await ctx.send('```Роли «' + role_name + '» на сервере нет, '
                       'можете создать ее!```')
    elif role_name not in [str(r.name) for r in ctx.message.author.roles]:
        await ctx.send('```' + author_nick + ', вы не состоите в роли «' + role_name + '» и не можете ее удалить.```')
    else:
        role_object = discord.utils.get(ctx.message.guild.roles, name=role_name)
        await role_object.delete()
        await ctx.send('```' + author_nick + ' удалил роль «' + role_name + '»```')
    await ctx.message.delete()


@bot.command()
async def hw(ctx, *args):
    await ctx.send(ctx.author.mention + ' приглашает ' + str(ctx.message.guild.default_role) + ' делать дз!')
    await ctx.message.delete()


print(discord.__version__)
print('Validation successful! Trying to run edc.bot...')
bot.run(TOKEN)
