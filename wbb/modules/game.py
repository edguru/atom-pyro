from aiogram.filters import Command
from aiogram.types import Message as Msgaio
from aiogram import F
from aiogram.types import InlineQuery, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultGame, CallbackQuery
import traceback

from wbb import app, LOG_GROUP_ID, atom, atombot








@atom.message(Command("aio"))
async def aio_test(message: Msgaio):
    await message.reply("works")
    

@atom.inline_query()
async def game_query_handler(query: InlineQuery):
    print("aio")
    try:
        text = query.query.strip().lower()
        print(text)
        buttons = InlineKeyboardMarkup(
        [
        [
        InlineKeyboardButton(
            text= "Play Flappy Bird", callback_game="flappy_bird"
            ),
        ],
        [
        InlineKeyboardButton(text ="Play with Friends", switch_inline_query_chosen_chat="" )
        ],
        [
        InlineKeyboardButton(text ="Play in Metakraft", url="https://t.me/metakraftdiscussions/19")
        ]])
        answ=[]
        answ.append(
        InlineQueryResultGame(
            type= "game",
            game_short_name= "flappy_bird",
            reply_markup=buttons,
        )
    )
        answe = answ
        print(answe)
        await query.answer(results=answe, cache_time=10)
    except Exception as e:
        print(e)
        await app.send_message(chat_id= LOG_GROUP_ID, text = e)




@atom.callback_query()
async def game_callback_handler(query: CallbackQuery):
    try:
        queid = query.id
        print(queid)
        que = query.game_short_name
        print(que)
        if que == "flappy_bird":
            return await query.answer(url= "https://games-meta.s3.amazonaws.com/games/flappy-64e1fc4d0f529e66f7ca0a67/index.html", cache_time= 12)
    except Exception as e:
        await app.send_message(chat_id= LOG_GROUP_ID, text = e)
