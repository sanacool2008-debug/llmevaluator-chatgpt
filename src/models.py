from pydantic import BaseModel,Field
from typing import Optional,List,Dict

class EvaluationResult(BaseModel):
    llm: str = Field(description="The LLM name")
    score: int = Field(description="The score of the LLM for the response")
    reason: str = Field(description="The reason for the score")

class EvaluationResponse(BaseModel):
    results: List[EvaluationResult] = Field(description="List of Evaluation Results")
    winner: str = Field(description="The winner of the llm response evaluation")

class LLMAnswer(BaseModel):
    answer: str = Field(description="LLM response")

class LlmRequest(BaseModel):
    prompt_template_name: str
    question: str

class LlmResponse(BaseModel):
    llm: str = Field(description="The LLM name")
    response: str = Field(description="The response from the LLM")

class LlmResponsesModel(BaseModel):
    llm_responses: List[LlmResponse] = Field(description="The List of LLM responses")
    prompt: str = Field(description="The prompt for the LLM")

class EvaluationRequest(BaseModel):
    model: str
    prompt_template_name: str
    llm_responses_model : LlmResponsesModel