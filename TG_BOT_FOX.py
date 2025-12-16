import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from aiogram import F
from NEWS import check_updates, get_first_news
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    start_buttons = ['Все новости за сутки', 'Последние пять', 'Политические новости']
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=btn)] for btn in start_buttons],
        resize_keyboard=True
    )
    await message.answer(
        "<b>Бот работает следующим образом:</b>\n"
        "• Автоматически собирает каждый час последние новости с главной страницы FOX.\n"
        "• С помощью команд можно вывести следующую информацию:\n"
        "  <i>Все новости за сутки, Последние пять, Политические новости</i>\n"
        "• Примечание: политические новости — это те, которые FOX отметил как политические и имеют значок \U0001F935.",
        reply_markup=keyboard
    )

my_dict_emoji = {
    'media': '\U0001F4E3',
    "politics": '\U0001F935',
    "us": '\U0001F5FD',
    "sports": '\U000026BD',
    "live-news": '\U00002B55',
    "food-drink": '\U0001F37D',
    "entertainment": '\U0001FA81'
}

@dp.message(F.text == 'Все новости за сутки')
async def get_all_news(message: types.Message):

    with open('news.json', 'r', encoding='utf-8') as file:
        news_dict = json.load(file)
    for k, v in news_dict.items():
        emoji = my_dict_emoji.get(v["Category"], '\U0001F4CD')
        news = (f"<b>{datetime.now().date().strftime('%d.%m.%Y')}</b>"
                f"\n{emoji} {v['Category']}"
                f'\n<a href="{v["Link"]}"><u>{k}</u></a>')
        await message.answer(news)

@dp.message(F.text == 'Последние пять')
async def get_last_five(message: types.Message):
    with open('news.json', 'r', encoding='utf-8') as file:
        news_dict = json.load(file)
    my_dict_emoji = {
        'media': '\U0001F4E3',
        "politics": '\U0001F935',
        "us": '\U0001F5FD',
        "sports": '\U000026BD',
        "live-news": '\U00002B55',
        "food-drink": '\U0001F37D',
        "entertainment": '\U0001FA81'
    }
    for k, v in list(news_dict.items())[-5:]:
        emoji = my_dict_emoji.get(v["Category"], '\U0001F4CD')
        news = (f"<b>{datetime.now().date().strftime('%d.%m.%Y')}</b>"
                f"\n{emoji} {v['Category']}"
                f'\n<a href="{v["Link"]}"><u>{k}</u></a>')
        await message.answer(news)



@dp.message(F.text == 'Политические новости')
async def politics(message: types.Message):
    with open('news.json', 'r', encoding='utf-8') as file:
        news_dict = json.load(file)
    counter= 0
    for k, v in list(news_dict.items()):
        if v['Category'] == 'politics':
            counter+=1
            news = (f"<b>{datetime.now().date().strftime('%d.%m.%Y')}</b>"
                    f"\U0001F935"
                    f'\n<a href="{v["Link"]}"><u>{k}</u></a>')
            await message.answer(news)
    if counter == 0:
        await message.answer('Нет политических новостей')


async def news_every_hour():
    while True:
        fresh_news = check_updates()
        if len(fresh_news) > 0:
            for k, v in fresh_news.items():
                emoji = my_dict_emoji.get(v["Category"], '\U0001F4CD')
                news = (f"<b>{datetime.now().date().strftime('%d.%m.%Y')}</b>"
                        f"\n{emoji} {v['Category']}"
                        f'\n<a href="{v["Link"]}"><u>{k}</u></a>')
                await bot.send_message(os.getenv('USER_ID'), news, disable_notification=True)
        else:
            await bot.send_message(os.getenv('USER_ID'), 'Ничего нового... пока что', disable_notification=True)
        await asyncio.sleep(3600)



async def clear_news_every_day():
    while True:
        with open('news.json', "w", encoding="utf-8") as f:
            json.dump({}, f)
        get_first_news()
        await asyncio.sleep(84600)

async def main():
    # фон для рассылки только на твой user_id
    asyncio.create_task(news_every_hour())
    asyncio.create_task(clear_news_every_day())
    # polling для всех пользователей
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())


