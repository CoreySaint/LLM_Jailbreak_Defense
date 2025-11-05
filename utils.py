from google import genai
from openai import OpenAI
from dotenv import load_dotenv
import os

class AiModelHelper:
    def __init__(self, model_name: str):
        load_dotenv()
        self.model_name = model_name

        if self.model_name == "Gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Missing GEMINI_API_KEY in environment variables.")
            self.client = genai.Client(api_key=api_key)

        elif self.model_name == "Qwen":
            api_key=os.getenv("QWEN_API_KEY")
            if not api_key:
                raise ValueError("Missing QWEN_API_KEY in environment variables.")
            self.client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1", 
                api_key=api_key
            )
            
        elif self.model_name == "GPT":
            api_key=os.getenv("GPT_API_KEY")
            if not api_key:
                raise ValueError("Missinng GPT_API_KEY in environment variables")
            self.client = OpenAI(
                base_url = "https://integrate.api.nvidia.com/v1",
                api_key = api_key
            )
        
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        

    def get_response(self, version: str, prompt: str):
        if not version:
            raise ValueError("Version not supported. Please select a model and a version in the sidebar")
        
        if self.model_name == "Gemini":
            response = self.client.models.generate_content(
                model=version, 
                contents=prompt
            )
            return response.text
        
        elif self.model_name == "Qwen":
            if not version:
                version = "qwen/qwen3-next-80b-a3b-thinking"
            response = self.client.chat.completions.create(
                model=version,
                messages=[{"role":"user","content":prompt}],
                temperature=0.6,
                top_p=0.7,
                max_tokens=4096,
                stream=False
            )
            return response.choices[0].message.content

        elif self.model_name == "GPT":
            if not version:
                version = "openai/gpt-oss-20b"
            response = self.client.chat.completions.create(
                model=version,
                messages=[{"role":"user","content":prompt}],
                temperature=1,
                top_p=1,
                max_tokens=4096,
                stream=False
            )
            return response.choices[0].message.content
        
        else:
            return "Model not supported"