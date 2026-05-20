import os
from urllib import response

from dotenv import load_dotenv

import google.generativeai as genai
from openai import OpenAI

from app.core.config import MODEL_REGISTRY

load_dotenv()


class LLMEngine:

    def generate(self, provider, prompt):

        if provider == "github_models":
            return self._generate_github_models(prompt)
        
        elif provider == "gemini":
            return self._generate_gemini(prompt)

        elif provider == "openai":
            return self._generate_openai(prompt)
        
        elif provider == "groq":
            return self._generate_groq(prompt)

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
    
    def _generate_groq(self, prompt):

        client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
        )

        return response.choices[0].message.content
    
    def _generate_github_models(self, prompt):

        client = OpenAI(

            api_key=os.getenv(
                "GITHUB_MODELS_TOKEN"
            ),

            base_url="https://models.inference.ai.azure.com"
        )

        response = client.chat.completions.create(

            model="gpt-4o",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content