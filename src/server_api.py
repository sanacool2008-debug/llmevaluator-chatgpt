from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.logger_setup import logger_setup
from src.llm_evaluator import get_llm_responses
from src.models import LlmResponsesModel, LlmRequest

logger = logger_setup(__name__)

app = FastAPI()

@app.post("/responses", response_model=LlmResponsesModel)
def get_llm_responses_with_prompt(request: LlmRequest):
    # Define only 3 models (removed local model)
    models = {
        "openrouter_deepseek": "deepseek/deepseek-chat-v3.1:free",
        "openrouter_nvidia": "nvidia/nemotron-nano-9b-v2:free",
        "openrouter_openai": "openai/gpt-oss-20b:free"
    }

    prompt, llm_responses = get_llm_responses(models, request.prompt_template_name, request.question)
    llm_responses = [{"llm": key, "response": llm_response} for key, llm_response in llm_responses.items()]
    return LlmResponsesModel(llm_responses=llm_responses, prompt=prompt)

# --- Plugin discovery endpoints ---
@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    return FileResponse(".well-known/ai-plugin.json", media_type="application/json")

@app.get("/openapi.yaml")
def openapi_spec():
    return FileResponse("openapi.yaml", media_type="text/yaml")

@app.get("/")
def root():
    return {"status": "ok", "message": "Multi-LLM Action (3 models) is running!"}
