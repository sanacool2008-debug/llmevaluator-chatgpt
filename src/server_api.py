from fastapi import FastAPI
from .logger_setup import logger_setup
from .llm_evaluator import EvaluationResponse,get_evaluator_response,get_llm_responses
from .models import LlmResponsesModel,LlmRequest,EvaluationRequest

logger = logger_setup(__name__)


app = FastAPI()

@app.post("/responses",response_model=LlmResponsesModel)
def get_llm_responses_with_prompt(request: LlmRequest):
    prompt, llm_responses = get_llm_responses(request.models,request.prompt_template_name,request.question)
    llm_responses =[{"llm":key,"response":llm_response} for key,llm_response in llm_responses.items()]
    llm_response_model = LlmResponsesModel(llm_responses=llm_responses,prompt=prompt)
    return llm_response_model

@app.post("/evaluate",response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest):
    response = get_evaluator_response(request.model,request.prompt_template_name,request.llm_responses_model.prompt,request.llm_responses_model.llm_responses)
    return response