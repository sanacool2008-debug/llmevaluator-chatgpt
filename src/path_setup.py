import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FPATH = os.path.join(ROOT_DIR, ".env")
SRC_DIR = os.path.join(ROOT_DIR, "src")
CONFIG_DIR = os.path.join(SRC_DIR, "config")
DATA_DIR = os.path.join(SRC_DIR, "data")
OUTPUTS_DIR = os.path.join(SRC_DIR, "outputs")
ARTICLE_FPATH = os.path.join(DATA_DIR, "article.md")
APP_CONFIG_FPATH = os.path.join(CONFIG_DIR, "config.yaml")
PROMPT_CONFIG_FPATH = os.path.join(CONFIG_DIR, "prompt_config.yaml")
LOG_DIR = os.path.join(SRC_DIR, "logs")
LOG_FPATH = os.path.join(LOG_DIR, "server.log")