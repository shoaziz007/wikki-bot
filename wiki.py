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

# Константы (Токен лучше держать в .env, но пока оставим так)
TOKEN = '8544805108:AAHS0NyFSg0GUdE8UQdd3qMA0NCbhTjl95c'
wikipedia.set_lang("ru")

dp = Dispatcher()

@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer("Привет! Пришли запрос, и я найду это в Wikipedia.")

@dp.message()
async def search_wikipedia(message: types.Message):
    try:
        # Wikipedia search возвращает кортеж (results, suggestion)
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
        text = page.summary[:500] + "..." # Увеличил лимит текста для информативности
        
        await message.answer(f"📌 *{title}*\n\n📖 {text}\n\n🔗 [Читать полностью]({url})", parse_mode="Markdown")
        
    except wikipedia.exceptions.DisambiguationError as many_variants:
        variants = ", ".join(many_variants.options[:5])
        await message.answer(f"Запрос слишком общий. Попробуйте уточнить:\n\n{variants}")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer(f"Произошла ошибка при поиске.")

async def main():
    # ВАЖНО: Создаем сессию и бота ТОЛЬКО внутри асинхронной функции
    # Это решает ошибку "no running event loop"
    connector = ProxyConnector.from_url("http://proxy.server:3128")
    session = AiohttpSession(connector=connector)
    
    bot = Bot(token=TOKEN, session=session)
    
    print("Бот запущен на PythonAnywhere через прокси...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")