import os

from dotenv import load_dotenv

import google.generativeai as genai
from openai import OpenAI

from app.core.config import MODEL_REGISTRY

load_dotenv()


class LLMEngine:

    def generate(self, provider, prompt):

        if provider == "gemini":
            return self._generate_gemini(prompt)

        elif provider == "openai":
            return self._generate_openai(prompt)

        else:
            raise Exception(f"Unsupported provider: {provider}")

    def _generate_gemini(self, prompt):

        api_key = os.getenv("GEMINI_API_KEY")

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            MODEL_REGISTRY["gemini"]
        )

        response = model.generate_content(prompt)

        return response.text

    def _generate_openai(self, prompt):

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        response = client.chat.completions.create(
            model=MODEL_REGISTRY["openai"],
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content