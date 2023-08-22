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

import asyncio
import os
from datetime import datetime
from random import shuffle

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserNotParticipant,
)
from pyrogram.types import (
    Chat,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    User,
)
import random
from wbb import SUDOERS , DEVS, WELCOME_DELAY_KICK_SEC, app
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.core.keyboard import ikb
from wbb.utils.dbfunctions import (
    captcha_off,
    captcha_on,
    del_welcome,
    get_captcha_cache,
    get_welcome,
    has_solved_captcha_once,
    is_captcha_on,
    is_gbanned_user,
    save_captcha_solved,
    set_welcome,
    update_captcha_cache,
    is_wel_on,
    wel_on,
    wel_off
)
from wbb.utils.filter_groups import welcome_captcha_group
from wbb.utils.functions import extract_text_and_keyb, generate_captcha

__MODULE__ = "Greetings"
__HELP__ = """
/captcha [ENABLE|DISABLE] - Enable/Disable captcha.

/set_welcome - Reply this to a message containing correct
format for a welcome message, check end of this message.

/del_welcome - Delete the welcome message.
/get_welcome - Get the welcome message.

**SET_WELCOME ->**

The format should be something like below.

````

**Hi** {name} Welcome to {chat}

~ #This separater (~) should be there between text and buttons, remove this comment also

button=[Duck, https://duckduckgo.com]
button2=[Github, https://github.com]

````

**NOTES ->**

for /rules, you can do /filter rules to a message
containing rules of your groups whenever a user
sends /rules, he'll get the message

Checkout /markdownhelp to know more about formattings and other syntax.
"""

DEFAULT_WELCOME_MESSAGES = [
    "{name} is here!",  # Discord welcome messages copied
    "Ready player {name}",
    "Genos, {name} is here.",
    "A wild {name} appeared.",
    "{name} came in like a Lion!",
    "{name} has joined your party.",
    "{name} just joined. Can I get a heal?",
    "{name} just joined the chat - asdgfhak!",
    "{name} just joined. Everyone, look busy!",
    "Welcome, {name}. Stay awhile and listen.",
    "Welcome, {name}. We were expecting you ( ͡° ͜ʖ ͡°)",
    "Welcome, {name}. We hope you brought pizza.",
    "Welcome, {name}. Leave your weapons by the door.",
    "Swoooosh. {name} just landed.",
    "Brace yourselves. {name} just joined the chat.",
    "{name} just joined. Hide your bananas.",
    "{name} just arrived. Seems OP - please nerf.",
    "{name} just slid into the chat.",
    "A {name} has spawned in the chat.",
    "Big {name} showed up!",
    "Where’s {name}? In the chat!",
    "{name} hopped into the chat. Kangaroo!!",
    "{name} just showed up. Hold my beer.",
    "Challenger approaching! {name} has appeared!",
    "It's a bird! It's a plane! Nevermind, it's just {name}.",
    "It's {name}! Praise the sun! \o/",
    "Never gonna give {name} up. Never gonna let {name} down.",
    "Ha! {name} has joined! You activated my trap card!",
    "Hey! Listen! {name} has joined!",
    "We've been expecting you {name}",
    "It's dangerous to go alone, take {name}!",
    "{name} has joined the chat! It's super effective!",
    "Cheers, love! {name} is here!",
    "{name} is here, as the prophecy foretold.",
    "{name} has arrived. Party's over.",
    "{name} is here to kick butt and chew bubblegum. And {name} is all out of gum.",
    "Hello. Is it {name} you're looking for?",
    "{name} has joined. Stay a while and listen!",
    "Roses are red, violets are blue, {name} joined this chat with you",
    "It's a bird! It's a plane! - Nope, its {name}!",
    "{name} Joined! - Ok.",  # Discord welcome messages end.
    "All Hail {name}!",
    "Hi, {name}. Don't lurk, Only Villans do that.",
    "{name} has joined the battle bus.",
    "A new Challenger enters!",  # Tekken
    "Ok!",
    "{name} just fell into the chat!",
    "Something just fell from the sky! - oh, its {name}.",
    "{name} Just teleported into the chat!",
    "Hi, {name}, show me your Hunter License!",
    "Welcome {name}, Leaving is not an option!",
    "Run Forest! ..I mean...{name}.",
    "Hey, {name}, Empty your pockets.",
    "Hey, {name}!, Are you strong?",
    "Call the Avengers! - {name} just joined the chat.",
    "{name} joined. You must construct additional pylons.",
    "Ermagherd. {name} is here.",
    "Come for the Snail Racing, Stay for the Chimichangas!",
    "Who needs Google? You're everything we were searching for.",
    "This place must have free WiFi, cause I'm feeling a connection.",
    "Speak friend and enter.",
    "Welcome you are",
    "Welcome {name}, your princess is in another castle.",
    "Hi {name}, welcome to the dark side.",
    "Hola {name}, beware of people with nation levels",
    "Hey {name}, we have the droids you are looking for.",
    "Hi {name}\nThis isn't a strange place, this is my home, it's the people who are strange.",
    "Oh, hey {name} what's the password?",
    "Hey {name}, I know what we're gonna do today",
    "{name} just joined, be at alert they could be a spy.",
    "{name} joined the group, read by Mark Zuckerberg, CIA and 35 others.",
    "Welcome {name}, Watch out for falling monkeys.",
    "Everyone stop what you’re doing, We are now in the presence of {name}.",
    "Hey {name}, Do you wanna know how I got these scars?",
    "Welcome {name}, drop your weapons and proceed to the spy scanner.",
    "Stay safe {name}, Keep 3 meters social distances between your messages.",  # Corona memes lmao
    "You’re here now {name}, Resistance is futile",
    "{name} just arrived, the force is strong with this one.",
    "{name} just joined on president’s orders.",
    "Hi {name}, is the glass half full or half empty?",
    "Yipee Kayaye {name} arrived.",
    "Welcome {name}, if you’re a secret agent press 1, otherwise start a conversation",
    "{name}, I have a feeling we’re not in Kansas anymore.",
    "They may take our lives, but they’ll never take our {name}.",
    "Coast is clear! You can come out guys, it’s just {name}.",
    "Welcome {name}, Pay no attention to that guy lurking.",
    "Welcome {name}, May the force be with you.",
    "May the {name} be with you.",
    "{name} just joined.Hey, where's Perry?",
    "{name} just joined. Oh, there you are, Perry.",
    "Ladies and gentlemen, I give you ...  {name}.",
    "Behold my new evil scheme, the {name}-Inator.",
    "Ah, {name} the Platypus, you're just in time... to be trapped.",
    "*snaps fingers and teleports {name} here*",
    "{name} just arrived. Diable Jamble!",  # One Piece Sanji
    "{name} just arrived. Aschente!",  # No Game No Life
    "{name} say Aschente to swear by the pledges.",  # No Game No Life
    "{name} just joined. El psy congroo!",  # Steins Gate
    "Irasshaimase {name}!",  # weeabo shit
    "Hi {name}, What is 1000-7?",  # tokyo ghoul
    "Come. I don't want to destroy this place",  # hunter x hunter
    "I... am... Whitebeard!...wait..wrong anime.",  # one Piece
    "Hey {name}...have you ever heard these words?",  # BNHA
    "Can't a guy get a little sleep around here?",  # Kamina Falls – Gurren Lagann
    "It's time someone put you in your place, {name}.",  # Hellsing
    "Unit-01's reactivated..",  # Neon Genesis: Evangelion
    "Prepare for trouble....And make it double",  # Pokemon
    "Hey {name}, Are You Challenging Me?",  # Shaggy
    "Oh? You're Approaching Me?",  # jojo
    "{name} just warped into the group!",
    "I..it's..it's just {name}.",
    "Sugoi, Dekai. {name} Joined!",
    "{name}, do you know Gods of death love apples?",  # Death Note owo
    "I'll take a potato chip.... and eat it",  # Death Note owo
    "Oshiete oshiete yo sono shikumi wo!",  # Tokyo Ghoul
    "Kaizoku ou ni...nvm wrong anime.",  # op
    "{name} just joined! Gear.....second!",  # Op
    "Omae wa mou....shindeiru",
    "Hey {name}, the leaf village lotus blooms twice!",  # Naruto stuff begins from here
    "{name} Joined! Omote renge!",
    "{name} joined!, Gate of Opening...open!",
    "{name} joined!, Gate of Healing...open!",
    "{name} joined!, Gate of Life...open!",
    "{name} joined!, Gate of Pain...open!",
    "{name} joined!, Gate of Limit...open!",
    "{name} joined!, Gate of View...open!",
    "{name} joined!, Gate of Shock...open!",
    "{name} joined!, Gate of Death...open!",
    "{name}! I, Madara! declare you the strongest",
    "{name}, this time I'll lend you my power. ",  # Kyuubi to naruto
    "{name}, welcome to the hidden leaf village!",  # Naruto thingies end here
    "In the jungle you must wait...until the dice read five or eight.",  # Jumanji stuff
    "Dr.{name} Famed archeologist and international explorer,\nWelcome to Jumanji!\nJumanji's Fate is up to you now.",
    "{name}, this will not be an easy mission - monkeys slow the expedition.",  # End of jumanji stuff
]


answers_dicc = []
loop = asyncio.get_running_loop()


async def get_initial_captcha_cache():
    global answers_dicc
    answers_dicc = await get_captcha_cache()
    return answers_dicc


loop.create_task(get_initial_captcha_cache())


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
@capture_err
async def welcome(_, message: Message):
    global answers_dicc

    # Get cached answers from mongodb in case of bot's been restarted or crashed.
    answers_dicc = await get_captcha_cache()

    # Mute new member and send message with button
    if not await is_captcha_on(message.chat.id):
        if await is_wel_on(message.chat.id):
            for member in message.new_chat_members:
                try:
                    if member.id in DEVS:
                           await message.reply_text(
                    f"{member.mention} A Member of Royal Family Just Arrived in the chat \n Status - Developers"
                )
                           continue
                    if member.id in SUDOERS:
                           await message.reply_text(
                    f"{member.mention} A Member of High Council Just landed in the chat \n Status - Sudo"
                )
                           continue

                    if await is_gbanned_user(member.id):
                        await message.chat.ban_member(member.id)
                        await message.reply_text(
                            f"{member.mention} was globally banned, and got removed,"
                            + " if you think this is a false gban, you can appeal"
                            + " for this ban in support chat."
                            )
                        continue

                    if member.is_bot:
                        if member.is_self:
                            await message.reply_text(f"{member.mention} I have just flown in")
                        else:
                            await message.reply_text(f"{member.mention} A bot was added")
                        continue
                    await send_welcome_message(message.chat, member.id, True )
                except Exception as e:
                    print(e)
        else:       
            return

    for member in message.new_chat_members:
        try:
            if member.id in SUDOERS:
                continue  # ignore sudo users

            if await is_gbanned_user(member.id):
                await message.chat.ban_member(member.id)
                await message.reply_text(
                    f"{member.mention} was globally banned, and got removed,"
                    + " if you think this is a false gban, you can appeal"
                    + " for this ban in support chat."
                )
                continue

            if member.is_bot:
                continue  # ignore bots

            # Ignore user if he has already solved captcha in this group
            # someday
            if await has_solved_captcha_once(message.chat.id, member.id):
                if not await is_wel_on(message.chat.id):
                    continue
                else:
                    await send_welcome_message(message.chat, member.id, True)
                continue

            await message.chat.restrict_member(member.id, ChatPermissions())
            text = (
                f"{(member.mention())} Are you human?\n"
                f"Solve this captcha in {WELCOME_DELAY_KICK_SEC} "
                "seconds and 4 attempts or you'll be kicked."
            )
        except ChatAdminRequired:
            return
        # Generate a captcha image, answers and some wrong answers
        captcha = generate_captcha()
        captcha_image = captcha[0]
        captcha_answer = captcha[1]
        wrong_answers = captcha[2]  # This consists of 8 wrong answers
        correct_button = InlineKeyboardButton(
            f"{captcha_answer}",
            callback_data=f"pressed_button {captcha_answer} {member.id}",
        )
        temp_keyboard_1 = [correct_button]  # Button row 1
        temp_keyboard_2 = []  # Botton row 2
        temp_keyboard_3 = []
        for i in range(2):
            temp_keyboard_1.append(
                InlineKeyboardButton(
                    f"{wrong_answers[i]}",
                    callback_data=f"pressed_button {wrong_answers[i]} {member.id}",
                )
            )
        for i in range(2, 5):
            temp_keyboard_2.append(
                InlineKeyboardButton(
                    f"{wrong_answers[i]}",
                    callback_data=f"pressed_button {wrong_answers[i]} {member.id}",
                )
            )
        for i in range(5, 8):
            temp_keyboard_3.append(
                InlineKeyboardButton(
                    f"{wrong_answers[i]}",
                    callback_data=f"pressed_button {wrong_answers[i]} {member.id}",
                )
            )

        shuffle(temp_keyboard_1)
        keyboard = [temp_keyboard_1, temp_keyboard_2, temp_keyboard_3]
        shuffle(keyboard)
        verification_data = {
            "chat_id": message.chat.id,
            "user_id": member.id,
            "answer": captcha_answer,
            "keyboard": keyboard,
            "attempts": 0,
        }
        keyboard = InlineKeyboardMarkup(keyboard)
        # Append user info, correct answer and
        answers_dicc.append(verification_data)
        # keyboard for later use with callback query
        button_message = await message.reply_photo(
            photo=captcha_image,
            caption=text,
            reply_markup=keyboard,
            quote=True,
        )
        os.remove(captcha_image)

        # Save captcha answers etc in mongodb in case bot gets crashed or restarted.
        await update_captcha_cache(answers_dicc)

        asyncio.create_task(
            kick_restricted_after_delay(WELCOME_DELAY_KICK_SEC, button_message, member)
        )
        await asyncio.sleep(0.5)


async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    raw_text = await get_welcome(chat.id)

    if not raw_text:
        mesg= random.choice(DEFAULT_WELCOME_MESSAGES)
        if "{chat}" in mesg:
            text = text.replace("{chat}", chat.title)
        if "{name}" in mesg:
            text = text.replace("{name}", (await app.get_users(user_id)).mention)
        async def _send_wait_dele():
            m = await app.send_message(
                chat.id,
                text=mesg,
                disable_web_page_preview=True,
            )
            await asyncio.sleep(300)
            await m.delete()
        asyncio.create_task(_send_wait_dele())
        return

    text, keyb = extract_text_and_keyb(ikb, raw_text)

    if "{chat}" in text:
        text = text.replace("{chat}", chat.title)
    if "{name}" in text:
        text = text.replace("{name}", (await app.get_users(user_id)).mention)

    async def _send_wait_delete():
        if keyb == "=":
            m = await app.send_message(
                chat.id,
                text=text,
                disable_web_page_preview=True,
            )
        else:
            m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
        await asyncio.sleep(300)
        await m.delete()

    asyncio.create_task(_send_wait_delete())


@app.on_callback_query(filters.regex("pressed_button"))
async def callback_query_welcome_button(_, callback_query):
    """After the new member presses the correct button,
    set his permissions to chat permissions,
    delete button message and join message.
    """
    global answers_dicc
    data = callback_query.data
    pressed_user_id = callback_query.from_user.id
    pending_user_id = int(data.split(None, 2)[2])
    button_message = callback_query.message
    answer = data.split(None, 2)[1]

    correct_answer = None
    keyboard = None

    if len(answers_dicc) != 0:
        for i in answers_dicc:
            if (
                i["user_id"] == pending_user_id
                and i["chat_id"] == button_message.chat.id
            ):
                correct_answer = i["answer"]
                keyboard = i["keyboard"]

    if not (correct_answer and keyboard):
        return await callback_query.answer("Something went wrong, Rejoin the " "chat!")

    if pending_user_id != pressed_user_id:
        return await callback_query.answer("This is not for you")

    if answer != correct_answer:
        await callback_query.answer("Yeah, It's Wrong.")
        for iii in answers_dicc:
            if (
                iii["user_id"] == pending_user_id
                and iii["chat_id"] == button_message.chat.id
            ):
                attempts = iii["attempts"]
                if attempts >= 3:
                    answers_dicc.remove(iii)
                    await button_message.chat.ban_member(pending_user_id)
                    await asyncio.sleep(1)
                    await button_message.chat.unban_member(pending_user_id)
                    await button_message.delete()
                    await update_captcha_cache(answers_dicc)
                    return

                iii["attempts"] += 1
                break

        shuffle(keyboard[0])
        shuffle(keyboard[1])
        shuffle(keyboard[2])
        shuffle(keyboard)
        keyboard = InlineKeyboardMarkup(keyboard)
        return await button_message.edit(
            text=button_message.caption.markdown,
            reply_markup=keyboard,
        )

    await callback_query.answer("Captcha passed successfully!")
    await button_message.chat.unban_member(pending_user_id)
    await button_message.delete()

    if len(answers_dicc) != 0:
        for ii in answers_dicc:
            if (
                ii["user_id"] == pending_user_id
                and ii["chat_id"] == button_message.chat.id
            ):
                answers_dicc.remove(ii)
                await update_captcha_cache(answers_dicc)

    chat = callback_query.message.chat

    # Save this verification in db, so we don't have to
    # send captcha to this user when he joins again.
    await save_captcha_solved(chat.id, pending_user_id)
    if not await is_wel_on(chat.id):
        return
    return await send_welcome_message(chat, pending_user_id, True)


async def kick_restricted_after_delay(delay, button_message: Message, user: User):
    """If the new member is still restricted after the delay, delete
    button message and join message and then kick him
    """
    global answers_dicc
    await asyncio.sleep(delay)
    join_message = button_message.reply_to_message
    group_chat = button_message.chat
    user_id = user.id
    await join_message.delete()
    await button_message.delete()
    if len(answers_dicc) != 0:
        for i in answers_dicc:
            if i["user_id"] == user_id:
                answers_dicc.remove(i)
                await update_captcha_cache(answers_dicc)
    await _ban_restricted_user_until_date(group_chat, user_id, duration=delay)


async def _ban_restricted_user_until_date(group_chat, user_id: int, duration: int):
    try:
        member = await group_chat.get_member(user_id)
        if member.status == ChatMemberStatus.RESTRICTED:
            until_date = int(datetime.utcnow().timestamp() + duration)
            await group_chat.ban_member(user_id, until_date=until_date)
    except UserNotParticipant:
        pass


@app.on_message(filters.command("captcha") & ~filters.private)
@adminsOnly("can_restrict_members")
async def captcha_state(_, message):
    usage = "**Usage:**\n/captcha [ENABLE|DISABLE]"
    if len(message.command) != 2:
        await message.reply_text(usage)
        return
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await captcha_on(chat_id)
        await message.reply_text("Enabled Captcha For New Users.")
    elif state == "disable":
        await captcha_off(chat_id)
        await message.reply_text("Disabled Captcha For New Users.")
    else:
        await message.reply_text(usage)

@app.on_message(filters.command("welcome") & ~filters.private)
@adminsOnly("can_restrict_members")
async def captcha_state(_, message):
    usage = "**Usage:**\n/welcome [ENABLE|DISABLE]"
    if len(message.command) != 2:
        await message.reply_text(usage)
        return
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await wel_on(chat_id)
        await message.reply_text("Enabled Welcome For New Users.")
    elif state == "disable":
        await wel_off(chat_id)
        await message.reply_text("Disabled Welcome For New Users.")
    else:
        await message.reply_text(usage)

# WELCOME MESSAGE


@app.on_message(filters.command("set_welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    usage = "You need to reply to a text, check the Greetings module in /help"
    if not message.reply_to_message:
        await message.reply_text(usage)
        return
    if not message.reply_to_message.text:
        await message.reply_text(usage)
        return
    chat_id = message.chat.id
    raw_text = message.reply_to_message.text.markdown
    if not (extract_text_and_keyb(ikb, raw_text)):
        return await message.reply_text("Wrong formating, check help section.")
    await set_welcome(chat_id, raw_text)
    await message.reply_text("Welcome message has been successfully set.")


@app.on_message(filters.command("del_welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def del_welcome_func(_, message):
    chat_id = message.chat.id
    await del_welcome(chat_id)
    await message.reply_text("Welcome message has been deleted.")


@app.on_message(filters.command("get_welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def get_welcome_func(_, message):
    chat = message.chat
    welcome = await get_welcome(chat.id)
    if not welcome:
        return await message.reply_text("No welcome message set.")
    if not message.from_user:
        return await message.reply_text("You're anon, can't send welcome message.")

    await send_welcome_message(chat, message.from_user.id)

    await message.reply_text(f'`{welcome.replace("`", "")}`')
