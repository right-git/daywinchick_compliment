import instructor
import asyncio
import random
import httpx
from pydantic import BaseModel

from telethon import TelegramClient, events
from loguru import logger
from langsmith.wrappers import wrap_openai
from openai import AsyncOpenAI

from config import API_ID, API_HASH, PHONE_NUMBER, BOT_CHAT_ID, BOT_TRIGGER_MESSAGE, GEMINI_API_KEY, PROXY, SYSTEM_PROMPT
from utils import get_image_base64

tg_client = TelegramClient(
    "account.session",
    API_ID,
    API_HASH,
    device_model="iPhone 15 Pro",
    system_version="IOS 18.1",
    app_version="11.6.2",
).start(phone=PHONE_NUMBER)


openai_client = wrap_openai(
    AsyncOpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=GEMINI_API_KEY,
        http_client=httpx.AsyncClient(proxy=PROXY, timeout=30),
    )
)
llm_client = instructor.from_openai(openai_client)

class LlmResponse(BaseModel):
    compliment_text: str

@tg_client.on(events.NewMessage(incoming=True))
async def handle_message(event: events.NewMessage.Event):
    """
    Handles new incoming messages.
    """
    if event.chat_id != BOT_CHAT_ID:
        return

    message_text = event.message.message

    logger.debug(message_text)
    llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if message_text.strip() == BOT_TRIGGER_MESSAGE.strip():
        logger.info("Generating compliment")
        last_3_messages = await tg_client.get_messages(BOT_CHAT_ID, limit=3)
        logger.debug(last_3_messages[2])
        bot_message = last_3_messages[2]
        message_caption = bot_message.message

        if hasattr(bot_message.media, "photo"):
            file_path = await bot_message.download_media(file=f"./image-{random.randint(-99999, 99999)}.png")
            base64_image = get_image_base64(file_path)

            llm_messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message_caption,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    }
                ]
            })
        else:
            llm_messages.append({
                "role": "user",
                "content": message_caption
            })


        response = await llm_client.chat.completions.create(
            model="gemini-2.0-flash",
            response_model=LlmResponse,
            messages=llm_messages
        )

        logger.debug(response)

        compliment = response.compliment_text

        await tg_client.send_message(BOT_CHAT_ID, compliment)





async def main():
    logger.info("Running...")
    await tg_client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())