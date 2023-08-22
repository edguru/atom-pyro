# flake8: noqa F405
"""
MIT License

Copyright (c) 2023 atom-pyro

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

import traceback

from wbb import app
from wbb.utils.inlinefuncs import *

__MODULE__ = "Inline"
__HELP__ = """See inline for help related to inline"""


@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.strip() == "":
            answerss = await inline_help_func(__HELP__)
            await client.answer_inline_query(query.id, results=answerss, cache_time=10)
        elif text.split()[0] == "alive":
            answerss = await alive_function(answers) 
            await client.answer_inline_query(query.id, results=answerss, cache_time=10)
        elif text.split()[0] == "google":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Google Search | google [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await google_search_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "speedtest":
            answerss = await speedtest_init(query)
            return await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "ping":
            answerss = await ping_func(answers)
            await client.answer_inline_query(query.id, results=answerss, cache_time=2)

        elif text.split()[0] == "info":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="User Info | info [USERNAME|ID]",
                    switch_pm_parameter="inline",
                )
            tex = text.split()[1].strip()
            answerss = await info_inline_func(answers, tex)
            await client.answer_inline_query(query.id, results=answerss, cache_time=2)
        
        elif text.strip() == "tasks":
            user_id = query.from_user.id
            answerss = await task_inline_func(user_id)
            await client.answer_inline_query(query.id, results=answerss, cache_time=1)
    except Exception as e:
        print(e)
