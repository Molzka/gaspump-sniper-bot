from aiogram import Bot, types

from ..config import CHANNEL_ID
from ..database.crud import (
    create_profile,
    edit_profile,
    get_profile,
    update_name_history,
    update_username_history,
)
from ..database.db import get_engine
from ..gaspump.cryptotokens import get_created_tokens, get_dev_suplai_crypto_data


async def check_subscription(user_id: int, bot: Bot):
    member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    return member.status in {"member", "creator", "administrator"}


async def get_user_info(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    engine = get_engine()
    await create_profile(engine, user_id)

    fullname = message.from_user.full_name or ""
    username = message.from_user.username or ""

    current_profile = await get_profile(engine, user_id)

    if fullname and current_profile.name != fullname:
        await update_name_history(engine, user_id, fullname)

    if username and current_profile.username != username:
        await update_username_history(engine, user_id, username)

    await edit_profile(
        engine,
        user_id,
        fullname,
        username,
    )


async def get_formatted_caption(data: dict):
    token_address = data["token_address"]
    name = data["name"]
    ticker = data["ticker"]
    description = data["description"]
    user_info = data["user_info"]
    telegram_id = user_info["telegram_id"]
    owner_name = user_info["name"]
    username = user_info["telegram_username"]
    wallet_address = user_info["wallet_address"]
    telegram = data.get("tg_channel_link", "N/A")
    twitter = data.get("twitter_link", "N/A")
    website = data.get("website_link", "N/A")

    dev_suplai = await get_dev_suplai_crypto_data(token_address)
    tokens = await get_created_tokens(telegram_id)

    return f"""<b>НОВЫЙ ТОКЕН ЗАЛИСТИЛСЯ🚀</b>

<b>✏️ Название:</b> {name}
<b>🪪 CA:</b> <code>{token_address}</code>
<b>📖 Ticker:</b> {ticker}
<b>💸 Dev suplai:</b> {dev_suplai["ton_deployed"]} TON - {round(dev_suplai["percent"], 2)}%
<b>📇 Описание:</b> {description}

<b>👤 Информация о пользователе:</b>
    - <b>Имя:</b> {owner_name}
    - <b>Токены:</b> {tokens["tokens"]}
    - <b>DeDust:</b> {tokens["dedust"]}
    - <b>TG Username:</b> @{username}
    - <b>TG ID:</b> {telegram_id}

<b>🏡 Адрес кошелька:</b> {wallet_address}

<b>📲 Tonviewer:</b> tonviewer.com/{wallet_address}

<b>📨 Соц сети:</b>
      <b>- Telegram:</b> {telegram}
      <b>- Twitter:</b> {twitter}
      <b>- Website:</b> {website}

<b>➡️ Go to Gas Pump: <a href="Gaspump.tg/#/token/trade?token_address={token_address}">Купить {ticker} на Gaspump</a></b>"""
