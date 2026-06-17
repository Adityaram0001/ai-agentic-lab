import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Ensure it loads from the root of the project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

if not AZURE_API_KEY:
    print("Warning: AZURE_OPENAI_API_KEY is not set. Please check your .env file.")

def get_langchain_llm(reasoning_effort="low", temperature=0.7):
    """
    Returns an AzureChatOpenAI instance configured for LangChain/LangGraph.
    Dynamically passes the reasoning_effort.
    """
    from langchain_openai import AzureChatOpenAI
    
    return AzureChatOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        temperature=temperature,
        model_kwargs={"reasoning_effort": reasoning_effort}
    )

def get_openai_client():
    """
    Returns a native OpenAI client configured for Azure.
    """
    from openai import AzureOpenAI
    return AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION
    )

def get_crewai_llm(reasoning_effort="low", temperature=0.7):
    """
    Returns an LLM instance for CrewAI.
    """
    return get_langchain_llm(reasoning_effort, temperature)

def get_autogen_config_list(reasoning_effort="low"):
    """
    Returns the config_list required by AutoGen.
    """
    return [{
        "model": AZURE_DEPLOYMENT_NAME,
        "api_key": AZURE_API_KEY,
        "base_url": AZURE_ENDPOINT,
        "api_type": "azure",
        "api_version": AZURE_API_VERSION,
        "reasoning_effort": reasoning_effort
    }]
