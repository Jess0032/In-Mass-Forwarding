import asyncio
import re
from telethon.sessions import StringSession
from telethon import events, Button
from telethon.tl import patched
from telethon.tl.custom import conversation
from telethon.events import NewMessage
from telethon import errors

from config import *

conversation = {}

def isdigit(string):
    return bool(re.match(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', string))

@bot.on(NewMessage(pattern='/forward'))
async def forward_all(event):
    try:
        async with bot.conversation(await event.get_chat()) as conv:
            global conversation
            params = {'reverse': True}
            conversation[event.peer_id.user_id] = conv
            await conv.send_message("Diga el chat desde donde desea reeviar. (ORIGEN)")
            text = (await conv.get_response()).raw_text
            params['entity'] = int(text) if isdigit(text) else text
            await conv.send_message("Diga el chat hacia donde desea reeviar. (DESTINO)")
            text = (await conv.get_response()).raw_text
            destiny = int(text) if isdigit(text) else text

            await conv.send_message('Desea reenviar por palabra clave o por ragon de id??', buttons=[
                                    Button.inline('PalabraClave', b'data_pc'),
                                    Button.inline('Rango de id', b'data_rango')])

            press = await conv.wait_event(events.CallbackQuery(func=lambda e: e.sender_id == event.peer_id.user_id, data=re.compile(b'data_')))
            await press.answer('eres pto')
            print(press.data)
            if press.data == b'data_pc':
                await conv.send_message("Diga la palabra  clave (se reenviará todo mensaje q lo contenga)")
                params['search'] = (await conv.get_response()).raw_text
            else:
                await conv.send_message("Diga el id del mensaje inicial")
                params['min_id'] = int((await conv.get_response()).raw_text)-1
                await conv.send_message("Diga el id del mensaje final")
                params['max_id'] = int((await conv.get_response()).raw_text)+1

        await forwardelements(destiny, params)

    except Exception as e:
        print(e)


@bot.on(NewMessage(pattern='/cancel'))
async def forward(event):
    try:
        conversation[event.peer_id.user_id].cancel()
        await event.respond("Cancelado")
    except Exception as e:
        print(e)


async def forwardelements(destiny, params):
    print('reenviando')
    count = 0
    async with TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH) as client:
        print(client.session.save())
        async for message in client.iter_messages(**params):
            if isinstance(message, patched.Message):
                try:
                    await client.send_message(entity=destiny, message=message)
                except errors.FloodWaitError as e:
                    print('Flood for', e.seconds)
                    await asyncio.sleep(e.seconds)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_forever()
