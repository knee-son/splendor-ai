from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

METADATA_DIR = Path(os.getenv("METADATA_DIR"))
SCRIPTS_DIR = Path(os.getenv("SCRIPTS_DIR"))

