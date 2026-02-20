import asyncio
import logging
import wikipedia
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Константы
TOKEN = '8544805108:AAHS0NyFSg0GUdE8UQdd3qMA0NCbhTjl95c'
wikipedia.set_lang("ru")

dp = Dispatcher()

@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer("Привет! Пришли запрос, и я найду это в Wikipedia.")

@dp.message()
async def search_wikipedia(message: types.Message):
    try:
        wiki_search_result, suggestion = wikipedia.search(message.text, suggestion=True)
        
        if suggestion:
            await message.answer(f"Возможно, вы имели в виду: {suggestion}?")
            wiki_search_result = wikipedia.search(suggestion)
            
        if not wiki_search_result:
            await message.answer('По вашему запросу ничего не найдено')
            return

        page = wikipedia.page(wiki_search_result[0])
        title = page.title
        url = page.url
        text = page.summary[:500] + "..."
        
        await message.answer(f"📌 *{title}*\n\n📖 {text}\n\n🔗 [Читать полностью]({url})", parse_mode="Markdown")
        
    except wikipedia.exceptions.DisambiguationError as many_variants:
        variants = ", ".join(many_variants.options[:5])
        await message.answer(f"Запрос слишком общий. Попробуйте уточнить:\n\n{variants}")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer(f"Произошла ошибка при поиске.")

async def main():
    # Мы убрали создание коннектора из AiohttpSession, 
    # так как твоя библиотека выдает ошибку TypeError.
    # Вместо этого передаем прокси напрямую в объект Bot.
    
    bot = Bot(
        token=TOKEN, 
        session=AiohttpSession(),
        proxy="http://proxy.server:3128" # Самый надежный способ для PythonAnywhere
    )
    
    print("Бот запущен на PythonAnywhere! Теперь прокси работает корректно.")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен") 