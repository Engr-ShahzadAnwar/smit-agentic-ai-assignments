import os
from dotenv import load_dotenv

from openai import AsyncOpenAI
from agents import (
    set_default_openai_client,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)

load_dotenv()

# ==================================================
# GEMINI OPENAI-COMPATIBLE CLIENT
# ==================================================

gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_default_openai_client(gemini_client)
set_tracing_disabled(True)

# ==================================================
# GLOBAL MODEL
# ==================================================

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=gemini_client
)

# ==================================================
# DIRECT HELPER FUNCTION
# ==================================================

async def ask_gemini(prompt: str):
    try:
        response = await gemini_client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"