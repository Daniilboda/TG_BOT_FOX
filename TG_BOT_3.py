import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from my_config import token, user_id
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from aiogram import F
from NEWS import check_updates, get_first_news
import asyncio
bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    start_buttons = ['Все новости', 'Последние пять', 'Свежие новости']
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=btn)] for btn in start_buttons],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

my_dict_emoji = {
    'media': '\U0001F4E3',
    "politics": '\U0001F935',
    "us": '\U0001F5FD',
    "sports": '\U000026BD',
    "live-news": '\U00002B55',
    "food-drink": '\U0001F37D',
    "entertainment": '\U0001FA81'
}

@dp.message(F.text == 'Все новости')
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

@dp.message(F.text == 'Свежие новости')
async def get_fresh(message: types.Message):
    fresh_news = check_updates()
    if len(fresh_news) > 0:
        for k, v in fresh_news.items():
            emoji = my_dict_emoji.get(v["Category"], '\U0001F4CD')
            news = (f"<b>{datetime.now().date().strftime('%d.%m.%Y')}</b>"
                f"\n{emoji} {v['Category']}"
                f'\n<a href="{v["Link"]}"><u>{k}</u></a>')
            await message.answer(news)
    else:
        await message.answer('Свежих новостей нет...')


async def news_every_minute():
    while True:
        fresh_news = check_updates()
        if len(fresh_news) > 0:
            for k, v in fresh_news.items():
                emoji = my_dict_emoji.get(v["Category"], '\U0001F4CD')
                news = (f"<b>{datetime.now().date().strftime('%d.%m.%Y')}</b>"
                        f"\n{emoji} {v['Category']}"
                        f'\n<a href="{v["Link"]}"><u>{k}</u></a>')
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, 'Ничего нового...', disable_notification=True)
        await asyncio.sleep(360)



async def clear_news_every_two_days():
    while True:
        with open('news.json', "w", encoding="utf-8") as f:
            json.dump({}, f)
        get_first_news()

        await asyncio.sleep(172800)

async def main():
    # фон для рассылки только на твой user_id
    asyncio.create_task(news_every_minute())
    asyncio.create_task(clear_news_every_two_days())
    # polling для всех пользователей
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())


