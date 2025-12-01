import time
from google import genai
from openai import OpenAI
from dotenv import load_dotenv
from defenses import JailbreakDefenses
import os

class AiModelHelper:
    def __init__(self, model_name: str):
        load_dotenv()
        self.model_name = model_name

        llama_key = os.getenv("LLAMA_API_KEY")
        if not llama_key:
            raise ValueError("Missing LLAMA_API_KEY (defensive model) in environment variables.")
                             
        self.defense_model = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1", 
                api_key=os.getenv("LLAMA_API_KEY")
            )
        self.defense = JailbreakDefenses(
            client = self.defense_model
        )

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
        

    def get_response(self, version: str, prompt: str, defense1: bool, defense2: bool):
        if not version:
            raise ValueError("Version not supported. Please select a model and a version in the sidebar")
        
        start = time.perf_counter()
        
        if defense1:
            try:
                flagged = self.defense.check_jailbreak(prompt)
            except Exception as e:
                print(f"Defense model error: {e}")
                flagged = False

            if not flagged:
                end = time.perf_counter()
                total_time = end - start
                return (f"Time to response: {total_time:.3f}  \n  The system detected this message as unsafe, please ensure your prompts follow the Terms of Service.")
            
        
        if self.model_name == "Gemini":
            response = self.client.models.generate_content(
                model=version, 
                contents=prompt
            )
            reply =  response.text
        
        elif self.model_name == "Qwen":
            if not version:
                version = "qwen/qwen3-235b-a22b"
            response = self.client.chat.completions.create(
                model=version,
                messages=[{"role":"user","content":prompt}],
                temperature=0.6,
                top_p=0.7,
                max_tokens=8192,
                stream=False
            )
            reply =  response.choices[0].message.content

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
            reply =  response.choices[0].message.content
        
        elif self.model_name == "Llama":
            if not version:
                version = "nvidia/llama-3.1-nemotron-safety-guard-8b-v3"
            response = self.client.chat.completions.create(
                model=version,
                messages=[{"role":"user","content":prompt}],
                temperature=1,
                top_p=1,
                max_tokens=4096,
                stream=False
            )
            reply = response.choices[0].message.content

        else:
            return "Model not supported"
        
        end = time.perf_counter()
        total_time = end - start
        formatted = f"Time to response: {total_time:.3f} seconds  \n  \n{reply}"
        return formatted

        