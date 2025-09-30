from src.utils import load_config,load_article,save_output,load_prompt_config
from src.llm_setup import set_models,set_evaluator_model
from src.models import EvaluationResponse

config = load_config()
prompt_config = load_prompt_config()

def lowercase_first_char(text: str) -> str:
    return text[0].lower() + text[1:] if text else text

def build_prompt(prompt_config):
    prompt_parts = []

    if role := prompt_config.get("role"):
        prompt_parts.append(f"Role:\nYou are {lowercase_first_char(role.strip())}.")

    instruction = prompt_config.get("instruction")

    if isinstance(instruction,list):
        formatted_instruction = "\n".join(f"- {item}" for item in instruction)
    else:
        formatted_instruction = instruction

    prompt_parts.append(f"Task:\n"+formatted_instruction)

    if constraints := prompt_config.get("output_constraints"):
        if isinstance(constraints, list):
            formatted_constraints = "\n".join(f"- {item}" for item in constraints)
        else:
            formatted_constraints = constraints

        prompt_parts.append(f"Output Constraints:\n"+ formatted_constraints)

    if tone := prompt_config.get("style_or_tone"):
        if isinstance(tone, list):
            formatted_tone = "\n".join(f"- {item}" for item in tone)
        else:
            formatted_tone = tone

        prompt_parts.append(f"Style & Tone:\n"+ formatted_tone)

    if goal := prompt_config.get("goal"):
        prompt_parts.append(f"Goal:\n{goal}")

    if template := prompt_config.get("template"):
        if isinstance(template, list):
            formatted_template = "\n".join(f"- {item}" for item in template)
        else:
            formatted_template = template
        prompt_parts.append(formatted_template)

    reasoning_strategy = prompt_config.get("reasoning_strategy")
    if reasoning_strategy and reasoning_strategy != "None" and config:
        strategies = config.get("reasoning_strategies", {})
        if strategy_text := strategies.get(reasoning_strategy):
            prompt_parts.append(strategy_text.strip())

    return "\n\n".join(prompt_parts)

def get_llm_responses(models,prompt_template_name,question):
    llms_dict = set_models(models)
    prompt_template = prompt_config[prompt_template_name]
    prompt = build_prompt(prompt_template).format(question=question)
    llm_responses_dict = {}
    for key, llm in llms_dict.items():
        response = llm.invoke(prompt)
        llm_responses_dict[key] = response.content
    return prompt,llm_responses_dict

def get_evaluator_response(model,prompt_template_name,llm_testing_prompt,llm_responses_dict):
    llm = set_evaluator_model(model=model)
    prompt_template = prompt_config[prompt_template_name]
    llm_response_str = "\n".join(f"- {llm_response.llm} : \n{llm_response.response}" for llm_response in llm_responses_dict)
    inputs = {
        "prompt": f"<<<BEGIN CONTENT>>>\n```\n +{llm_testing_prompt} \n```\n<<<END CONTENT>>>",
        "llm_responses": llm_response_str
    }
    prompt = build_prompt(prompt_template).format(**inputs)
    llm_struct = llm.with_structured_output(EvaluationResponse)
    try:
        eval_response = llm_struct.invoke(prompt)
    except Exception as e:
        print("Structured output parsing failed:", e)
        print("Raw prompt sent to LLM:\n", prompt)
        eval_response = None
    return eval_response


if __name__ == "__main__":
    prompt_template_name = 'prompt_config_llm_test'
    question = "A is heavier than B. C is lighter than D. B is heavier than C. D is lighter than E. Can you rank the five items from heaviest to lightest? Then, using only the five facts provided, explain whether it is possible to determine the relative weights of A and E."
    # question = "Compare the advantages and disadvantages of solar energy versus wind energy in a concise paragraph."
    # question = "If a company increases its revenue by 20% every year and starts with $100,000 in revenue, what will its revenue be after 5 years?"
    question = f"""Summarize the main points of the following paragraph in exactly 50 words.
“Climate change refers to long-term alterations in temperature, precipitation, wind patterns, and other elements of the Earth’s climate system. It can be caused by natural processes or human activities, and it impacts ecosystems, weather events, and global health."""
    # models = config["models"]
    prompt = build_prompt(prompt_config.get("prompt_config_llm_evaluation")).format(prompt="",llm_responses="")
    print(prompt)
    # llm_testing_prompt, llm_responses_dict = get_llm_responses(models,prompt_template_name,question)
    # evaluator_model = config["evaluator"]["openrouter_nvidia"]
    # prompt_template_eval_name = 'prompt_config_llm_evaluation'
    # evaluator_response = get_evaluator_response(evaluator_model, prompt_template_eval_name,llm_testing_prompt,llm_responses_dict)
    # print(f"Question:\n - {question}")
    # print(f"\n\nResponses from each LLM:\n{"\n".join(f"- LLM Name:{key} Response: {response}" for key,response in llm_responses_dict.items())}")
    # print(f"\n\nEvaluation Results:\n Winner :{evaluator_response.winner}\n Scores:\n{"\n".join(f"- LLM Name:{result.llm} Score: {result.score} Reason: {result.reason}" for result in evaluator_response.results)}")


