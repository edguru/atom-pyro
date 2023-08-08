from pyrogram import Client, filters
from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions

telegraph = Telegraph()
r = telegraph.create_account(short_name=atom-pyro)
auth_url = r["auth_url"]

TMP_DOWNLOAD_DIRECTORY = "./"
app = Client("session_name")

@app.on_message(filters.command("t", prefixes="/"))
async def telegraph_handler(client, message):
    if message.forward_from:
        return
    optional_title = message.text.split(None, 1)[1] if len(message.command) > 1 else None

    if message.reply_to_message:
        start = datetime.now()
        reply_message = message.reply_to_message

        if message.command[0] == "tm":
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
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await h.edit(f"Uploaded to https://telegra.ph{media_urls[0]}", link_preview=True)

        elif message.command[0] == "txt":
            user_object = await client.get_users(user_ids=reply_message.from_user.id)
            title_of_page = user_object.first_name

            if optional_title:
                title_of_page = optional_title

            page_content = reply_message.text

            if reply_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await client.download_media(
                    message=reply_message,
                    file_name=TMP_DOWNLOAD_DIRECTORY
                )

                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()

                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"

                os.remove(downloaded_file_name)

            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await message.reply(f"Pasted to https://telegra.ph/{response['path']} in {ms} seconds.", link_preview=True)

    else:
        await message.reply("Reply to a message to get a permanent telegra.ph link.")

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

help = """
I can upload files to Telegraph
 ❍ /tm :Get Telegraph Link Of Replied Media
 ❍ /txt :Get Telegraph Link of Replied Text
"""

mod_name = "Telegraph"

app.run()
