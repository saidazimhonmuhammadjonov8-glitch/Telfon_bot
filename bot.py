import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import os

# Muhim sozlamalar
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# /start komandasi
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📱 Telefon sotmoqchiman", "🔎 Telefon olmoqchiman")
    await message.answer("Assalomu alaykum!\nTelefon savdo botiga xush kelibsiz!", reply_markup=kb)

# Telefon sotish
@dp.message_handler(lambda msg: msg.text == "📱 Telefon sotmoqchiman")
async def sell_handler(message: types.Message):
    await message.answer("Telefoningiz haqida ma'lumotni yuboring.\nAdmin ko‘rib chiqadi va tasdiqlasa joylanadi.")

# Telefon olish
@dp.message_handler(lambda msg: msg.text == "🔎 Telefon olmoqchiman")
async def buy_handler(message: types.Message):
    await message.answer("Telefonlarni narx bo‘yicha filtrlab tanlashingiz mumkin:\n"
                         "0–500 ming\n500 ming–1 mln\n1 mln–3 mln\n3 mln dan yuqori.")

# Faqat admin ko‘ra oladigan xabarlar
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def forward_to_admin(message: types.Message):
    if message.chat.id != ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"Yangi e'lon:\n\n{message.text}")
        await message.answer("E'loningiz adminga yuborildi. Tasdiqlansa joylanadi ✅")

# Admin tasdiqlasa
@dp.message_handler(lambda msg: msg.chat.id == ADMIN_ID and msg.text.startswith("tasdiq"))
async def approve_handler(message: types.Message):
    text = message.text.replace("tasdiq", "").strip()
    if text:
        await bot.send_message(CHANNEL_ID, text)
        await message.answer("E'lon kanalga joylandi ✅")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
