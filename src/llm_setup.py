import os
from src.path_setup import ENV_FPATH,APP_CONFIG_FPATH
from langchain_openai import ChatOpenAI
from src.logger_setup import log_call_with_time,logger_setup
from dotenv import load_dotenv
from src.utils import load_config

load_dotenv(ENV_FPATH, override=True)

logger = logger_setup(__name__)

openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if openrouter_api_key:
    print(f"Openrouter API Key exists and begins {openrouter_api_key[:9]}")
else:
    print("Openrouter API Key not found")


@log_call_with_time
def set_models(models,temperature=0.0):
    chat_llms_dict = {}
    for key,model_name in models.items():
        if key == "local":
            print(f"Setting local model to {model_name}")
            chat_llm = ChatOpenAI(
                base_url="http://localhost:11434/v1",
                model=model_name,
                temperature=temperature,
                api_key="ollama"
            )
            chat_llms_dict[key] = chat_llm
        else:
            print(f"Setting model to {model_name}")
            chat_llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                model=model_name,
                temperature=temperature,
                api_key=openrouter_api_key
            )
            chat_llms_dict[key] = chat_llm

    return chat_llms_dict

def set_evaluator_model(model,temperature=0.0):
    print(f"Setting model to {model}")
    return ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                model=model,
                temperature=temperature,
                api_key=openrouter_api_key
            )

if __name__ == "__main__":
    config = load_config(APP_CONFIG_FPATH)
    models =config["models"]
    print(models)
    llms_dict = set_models(models)
    prompt = "Who are you?"
    print(f"Question: {prompt}")
    for key,llm in llms_dict.items():
        response = llm.invoke(prompt)
        print(f"{key} LLM Response: {response.content}")
    print("LLM Init completed")


