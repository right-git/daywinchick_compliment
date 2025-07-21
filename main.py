import instructor
import asyncio
import random
import httpx
from pydantic import BaseModel

from telethon import TelegramClient, events
from rich.console import Console
from rich.panel import Panel
from langsmith.wrappers import wrap_openai
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from config import (
    API_ID,
    API_HASH,
    PHONE_NUMBER,
    BOT_CHAT_ID,
    BOT_TRIGGER_MESSAGE,
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    PROXY,
    SYSTEM_PROMPT,
)
from utils import get_image_base64

console = Console()

tg_client = TelegramClient(
    "account.session",
    API_ID,
    API_HASH,
    device_model="iPhone 15 Pro",
    system_version="IOS 18.1",
    app_version="11.6.2",
)


openai_client = wrap_openai(
    AsyncOpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        http_client=httpx.AsyncClient(proxy=PROXY, timeout=30) if PROXY else None,
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

    llm_messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if message_text.strip() == BOT_TRIGGER_MESSAGE.strip():
        console.print("✨ [bold yellow]Generating compliment...[/bold yellow]")
        last_3_messages = await tg_client.get_messages(BOT_CHAT_ID, limit=3)

        if (
            not last_3_messages
            or not isinstance(last_3_messages, list)
            or len(last_3_messages) < 2
        ):
            console.print(
                "⚠️ [bold red]Not enough messages to generate a compliment.[/bold red]"
            )
            return

        target_message = last_3_messages[2]  # The message before the trigger
        message_caption = target_message.message

        if hasattr(target_message.media, "photo"):
            file_path = await target_message.download_media(
                file=f"./image-{random.randint(-99999, 99999)}.png"
            )
            base64_image = get_image_base64(file_path)

            llm_messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message_caption or ""},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            )
        else:
            llm_messages.append(
                {
                    "role": "user",
                    "content": [{"type": "text", "text": message_caption or ""}],
                }
            )

        response = await llm_client.chat.completions.create(
            model=LLM_MODEL, response_model=LlmResponse, messages=llm_messages
        )

        compliment = response.compliment_text
        await tg_client.send_message(BOT_CHAT_ID, compliment)
        console.print(f"💌 [bold green]Compliment sent![/bold green]\n> {compliment}")


async def main():
    console.print(
        Panel(
            "[bold cyan]✨ Daywinchick Compliment Bot ✨[/bold cyan]\n[dim]Waiting for trigger message...[/dim]",
            expand=False,
            border_style="magenta",
        )
    )
    if not tg_client.is_connected():
        await tg_client.start()
    await tg_client.run_until_disconnected()  # type: ignore


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
