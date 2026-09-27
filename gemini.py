from google import genai
from dotenv import load_dotenv
import os

load_dotenv()


def api():
    return os.getenv("GEMINI_KEY")

print(api())

ai_client = genai.Client(api_key=api())


def response(text):

    interaction = ai_client.interactions.create(
        input= f'''You are a helpful ai assistant who help users requests. User Query: {text}''',
        model="gemini-3.1-flash-lite"
    )

    return interaction.output_text
