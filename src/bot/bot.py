import asyncio
import datetime
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..config import BOT_TOKEN
from ..database.crud import get_ids
from ..database.db import db_start, get_engine
from ..gaspump.cryptotokens import get_crypto_data
from .utils import check_subscription, get_formatted_caption, get_user_info

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

last_token: str = ""


@dp.callback_query()
async def process_command(callback: types.CallbackQuery):
    logging.info(f"{datetime.datetime.now().ctime()} - Callback - {callback.data}")
    if callback.data == "check_sub":
        is_sub = await check_subscription(callback.from_user.id, bot)
        if is_sub:
            await bot.send_message(
                callback.from_user.id,
                text="""<b>Отлично! 
                                   
Теперь ты в курсе всех наших новостей и акций. 🚀</b>""",
            )


@dp.message(CommandStart())
async def user_start(message: types.Message):
    is_sub = await check_subscription(message.from_user.id, bot)

    if is_sub:
        await bot.send_message(message.from_user.id, "Добро пожаловать!")
    else:
        sub_inline_btn = InlineKeyboardButton(
            text="Я подписался!✅", callback_data="check_sub"
        )
        sub_inline_kb = InlineKeyboardMarkup(inline_keyboard=[[sub_inline_btn]])
        await bot.send_message(
            message.from_user.id,
            """<b>НОВЫЙ МЕМ КОИН? 🚀</b>

Мы уже в курсе! 

<b>Подпишись и не пропусти ни одного пампа: @gassboom 🧨</b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=sub_inline_kb,
        )
    await get_user_info(message, bot)


async def send_message_to_all(data):
    engine = get_engine()
    users = await get_ids(engine)
    photo = data["image_url"]
    caption = await get_formatted_caption(data)

    for user_id in users:
        try:
            if True:
                await bot.send_photo(
                    user_id, photo=photo, caption=caption, parse_mode=ParseMode.HTML
                )
        except Exception as e:
            logging.error(
                f"{datetime.datetime.now().ctime()} - Ошибка при отправке сообщения пользователю {user_id}: {e}"
            )


async def scheduled(wait_for):
    global last_token
    while True:
        try:
            data = await get_crypto_data()
        except Exception as e:
            logging.error(str(e))
        logging.info(f"{datetime.datetime.now().ctime()} - last_token: {last_token}")
        try:
            if data and last_token != data:
                await send_message_to_all(data[0])
                last_token = data
        except Exception as e:
            logging.error(
                f"{datetime.datetime.now().ctime()} - Ошибка при проверке токена: {e}, data - {data}, last_token = {last_token}"
            )
        await asyncio.sleep(wait_for)


async def start_bot():
    global last_token
    last_token = await get_crypto_data()
    await db_start()
    asyncio.create_task(scheduled(30))
    await dp.start_polling(bot)
