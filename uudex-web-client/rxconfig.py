import reflex as rx
from dotenv import load_dotenv
import os
from pathlib import Path

# Check for custom env file
env_file = os.getenv("ENVFILE")
if env_file:
    env_path = Path(env_file)
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_file}")
    print(f"Loading environment from: {env_file}")
    load_dotenv(env_file)
else:
    # Default to .env
    if Path(".env").exists():
        print("Loading environment from .env")
        load_dotenv()
    else:
        print("No environment file found, using defaults")

# Create config with app name only - environment vars will override defaults
config = rx.Config(
    app_name="uudex_web_client",
)
