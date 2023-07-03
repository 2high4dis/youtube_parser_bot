from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from youtube_search import YoutubeSearch
import hashlib


def searcher(text):
    res = YoutubeSearch(f'{text}', max_results=10).to_dict()
    return res


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = searcher(text)

    articles = [InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://youtube.com/watch?v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=InputTextMessageContent(
            message_text=f'https://youtube.com/watch?v={link["id"]}'
        )
    ) for link in links]

    await query.answer(articles, cache_time=30, is_personal=True)

executor.start_polling(dp, skip_updates=True)
