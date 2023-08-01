"""
MIT License

Copyright (c) 2023 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.utils.http import get

__MODULE__ = "Repo"
__HELP__ = "/repo - To Get My Github Repository Link " "And Support Group Link"


@app.on_message(filters.command("repo"))
@capture_err
async def repo(_, message):
    users = await get(
        "https://api.github.com/repos/thehamkercat/williambutcherbot/contributors"
    )
    list_of_users = ""
    count = 1
    for user in users:
        list_of_users += f"**{count}.** [{user['login']}]({user['html_url']})\n"
        count += 1

    text = f"""[Github](https://github.com/thehamkercat/WilliamButcherBot) | [Group](t.me/PatheticProgrammers)
```----------------
| Contributors |
----------------```
{list_of_users}"""
    await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
