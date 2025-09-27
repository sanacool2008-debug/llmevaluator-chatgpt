import os
import yaml
from .path_setup import ARTICLE_FPATH,APP_CONFIG_FPATH,OUTPUTS_DIR,PROMPT_CONFIG_FPATH
from .logger_setup import logger_setup,log_call_with_time
from typing import Optional

logger = logger_setup(__name__)

@log_call_with_time
def load_article(article_fpath=ARTICLE_FPATH):
    with open(article_fpath) as file:
        article = file.read()
    return article

@log_call_with_time
def load_config(config_fpath=APP_CONFIG_FPATH):
    with open(config_fpath,"r",encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config

@log_call_with_time
def load_prompt_config(prompt_config_path=PROMPT_CONFIG_FPATH):
    with open(prompt_config_path,"r",encoding="utf-8") as file:
        prompt_config = yaml.safe_load(file)
    return prompt_config

@log_call_with_time
def save_output(filename,text,output_dir=OUTPUTS_DIR,header:Optional[str]=None):
    os.makedirs(output_dir, exist_ok=True)
    outputfilepath = os.path.join(output_dir, filename)
    with open(outputfilepath, 'w',encoding='utf-8') as file:
        if header:
            file.write(f"# {header}\n")
            file.write("# " + "*" * 60 + "\n\n")
        file.write(text)



if __name__ == "__main__":
    config = load_config(APP_CONFIG_FPATH)
    print(config["models"]["local"])