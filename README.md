# 💌 Daywinchick Compliment Bot 💌

A sophisticated Telegram bot that uses a multimodal AI model to generate and send thoughtful compliments in a designated chat.

## ✨ Features

-   **🤖 Smart Compliments**: Leverages a powerful LLM to generate unique and context-aware compliments.
-   **🖼️ Multimodal Support**: Can analyze both text and images to create more personalized messages.
-   ** TRIGGER-BASED**: Activates only when a specific trigger message is sent, keeping chats clean.
-   **⚙️ Highly Configurable**: Easily set up with your own Telegram account, target chat, and AI model via environment variables.
-   **🔒 Privacy-Focused**: Designed to run on a user account, ensuring you have full control over its activity.

## 🚀 How It Works

1.  The bot continuously listens for new messages in the chat specified by `BOT_CHAT_ID`.
2.  When it detects the `BOT_TRIGGER_MESSAGE`, it wakes up.
3.  It fetches the message sent *right before* the trigger message.
4.  If the message contains an image, it's converted to base64 and sent to the AI model along with its caption. If it's just text, only the text is sent.
5.  The AI model, guided by the `SYSTEM_PROMPT`, generates a compliment.
6.  The bot sends the generated compliment back to the chat.

## 🛠️ Setup & Installation

Follow these steps to get your compliment bot up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/daywinchick_compliment.git
cd daywinchick_compliment
```

### 2. Set Up Environment

This project uses `uv` for package management.

```bash
# Install uv if you don't have it
pip install uv

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt # Or `uv pip install -p pyproject.toml`
```

### 3. Configure Environment Variables

You need to provide your credentials for Telegram and the LLM.

```bash
# Copy the example .env file
cp .env.example .env
```

Now, open the `.env` file and fill in the following values:

-   `API_ID` & `API_HASH`: Get these from [my.telegram.org](https://my.telegram.org).
-   `PHONE_NUMBER`: Your Telegram phone number in international format (e.g., `+1234567890`).
-   `BOT_CHAT_ID`: The ID of the target chat. You can get this from a bot like `@userinfobot`.
-   `BOT_TRIGGER_MESSAGE`: The exact text that will trigger the compliment generation.
-   `LLM_API_KEY`: Your API key for the language model.
-   `LLM_BASE_URL`: The base URL for the LLM API endpoint.
-   `LLM_MODEL`: The specific model to use (e.g., `gpt-4o`).
-   `SYSTEM_PROMPT`: The instruction prompt for the AI model.
-   `PROXY` (Optional): If you need a proxy to access the LLM API.

## ▶️ Usage

Once everything is configured, simply run the main script:

```bash
python main.py
```

The bot will connect to your Telegram account and start listening for the trigger message in the specified chat. Enjoy spreading positivity! ✨
