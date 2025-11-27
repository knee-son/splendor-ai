import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

env_path = Path(find_dotenv())
load_dotenv(env_path)

FRONTEND_TUNNEL_URL = os.getenv("FRONTEND_TUNNEL_URL")
