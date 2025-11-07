import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

METADATA_DIR = Path(os.getenv("METADATA_DIR"))
SCRIPTS_DIR = Path(os.getenv("SCRIPTS_DIR"))
