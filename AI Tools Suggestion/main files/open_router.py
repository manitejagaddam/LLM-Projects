from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

def open_router(model_name = "deepseek/deepseek-r1-0528:free", family = "deepseek"):
    open_router_model_client =  OpenAIChatCompletionClient(
        base_url="https://openrouter.ai/api/v1",
        model= model_name,
        api_key = OPEN_ROUTER_API_KEY,
        model_info={
            "family":family,
            "vision" :True,
            "function_calling":True,
            "json_output": False
        }
    )
    
    return open_router_model_client

