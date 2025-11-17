import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

env_path = Path(find_dotenv())
load_dotenv(env_path)

BASE_DIR = env_path.parent

METADATA_DIR = BASE_DIR / Path(os.getenv("METADATA_DIR"))
SCRIPTS_DIR = BASE_DIR / Path(os.getenv("SCRIPTS_DIR"))
IMAGE_INPUT = BASE_DIR / Path(os.getenv("IMAGE_INPUT"))
IMAGE_OUTPUT = BASE_DIR / Path(os.getenv("IMAGE_OUTPUT"))
