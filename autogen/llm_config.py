import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# AutoGen expects a list of configuration dictionaries
config_list = [
    {
        "model": os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-5-nano"),
        "api_key": os.getenv("AZURE_API_KEY"),
        "base_url": os.getenv("AZURE_ENDPOINT"),
        "api_type": "azure",
        "api_version": os.getenv("AZURE_API_VERSION", "2025-01-01-preview"),
        "temperature": 1.0,
    }
]

# The full LLM config object passed to agents
llm_config = {
    "config_list": config_list,
    "temperature": 1.0,
}
