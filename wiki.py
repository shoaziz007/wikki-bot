import asyncio
import logging
import wikipedia
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession


logging.basicConfig(level=logging.INFO)

TOKEN = '8544805108:AAHS0NyFSg0GUdE8UQdd3qMA0NCbhTjl95c'

bot = Bot(token=TOKEN)
dp = Dispatcher()
session = AiohttpSession(proxy="http://proxy.server:3128")
wikipedia.set_lang("ru")
skip_updates=True
suggestion=True

@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer("Привет пришли запрос!")


@dp.message()
async def search_wikipedia(message: types.Message):
    try:
        wiki_search_result, suggestion = wikipedia.search(message.text, suggestion=True)
        
        # Если Wikipedia нашла опечатку
        if suggestion:
            await message.answer(f"Возможно, вы имели в виду: {suggestion}?")
            # Обновляем наш список результатов поиском по исправленному слову
            wiki_search_result = wikipedia.search(suggestion)
            
        if not wiki_search_result:
            await message.answer('По вашему запросу ничего не найдено')
            return

        # Теперь wiki_search_result точно содержит данные (либо оригинальные, либо исправленные)
        page = wikipedia.page(wiki_search_result[0])
        title = page.title
        url = page.url
        text = page.summary[:250] + "..."
        
        await message.answer(f"Название: {title}\n\n🔗 Ссылка: {url}\n\n📖 Информация: {text}")
        
    except wikipedia.exceptions.DisambiguationError as many_variants:
        many_variants_error = ", ".join(many_variants.options[:5])
        await message.answer(f"Запрос слишком общий. Уточните:\n\n{many_variants_error}")
        
    except Exception as other_errors:
        await message.answer(f"Произошла ошибка: {other_errors}")
      
        
async def wiki():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(wiki())
 
 






