import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from pyrogram import filters
from pyrogram.types import Message
from wbb import app, tgraph
from wbb.core.decorators.errors import capture_err

__MODULE__ = "wiki"
__HELP__ = "/wiki search query"

@app.on_message(filters.command("wiki"))
@capture_err
async def wiki(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("**Usage:**\n /wiki query")
    else:
        search = message.text
    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        message.reply_text(
            "Disambiguated pages found! Adjust your query accordingly.\n<i>{}</i>".format(
                e
            ),
            parse_mode=ParseMode.HTML,
        )
    except PageError as e:
        message.reply_text(
            "<code>{}</code>".format(e), parse_mode=ParseMode.HTML
        )
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">Read more...</a>"""
        if len(result) > 4000:
            with open("result.txt", "w") as f:
                f.write(f"{result}\n\nUwU OwO OmO UmU")
            with open("result.txt", "rb") as f:
                app.send_document(
                    document=f,
                    filename=f.name,
                    reply_to_message_id=message.id,
                    chat_id=message.chat.id,
                    parse_mode=ParseMode.HTML,
                )
        else:
            message.reply_text(
                result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )


