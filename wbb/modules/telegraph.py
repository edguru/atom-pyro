from pyrogram import filters
from pyrogram.types import Message
import datetime
from wbb import app, tgraph
from wbb.core.decorators.errors import capture_err
from telegraph import upload_file, exceptions
from PIL import Image

__MODULE__ = "Telegraph"
__HELP__ = "/telegraph [Page name]: Paste styled text on telegraph."
TMP_DOWNLOAD_DIRECTORY = "./"

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


@app.on_message(filters.command("telegraph"))
@capture_err
async def paste(_, message: Message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply("Reply to a text message")

    if len(message.command) < 2:
        return await message.reply("**Usage:**\n /telegraph [Page name]")

    page_name = message.text.split(None, 1)[1] 
    if reply.text :   
        page = tgraph.create_page(
        page_name, html_content=reply.text.html.replace("\n", "<br>")
    )
    else :
        start = datetime.now()
        downloaded_file_name = await client.download_media(
                message=reply_message,
                file_name=TMP_DOWNLOAD_DIRECTORY
            )
        end = datetime.now()
        ms = (end - start).seconds
        h = await message.reply(f"Downloaded to {downloaded_file_name} in {ms} seconds.")
        if downloaded_file_name.endswith((".webp")):
             resize_image(downloaded_file_name)
        try:
            start = datetime.now()
            media_urls = upload_file(downloaded_file_name)
        except exceptions.TelegraphException as exc:
            await h.edit("ERROR: " + str(exc))
            os.remove(downloaded_file_name)
            return
        end = datetime.now()
        ms_two = (end - start).seconds
        os.remove(downloaded_file_name)
        return await h.edit(f"Uploaded to https://telegra.ph{media_urls[0]}", link_preview=True)
        
    return await message.reply(
        f"**Posted:** {page['url']}",
        disable_web_page_preview=True,
    )
