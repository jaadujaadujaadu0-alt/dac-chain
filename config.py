import os
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.getenv("APP_URL", "https://inception.dachain.io/")
FAUCET_URL = os.getenv("FAUCET_URL", "https://inception.dachain.io/faucet")
EXCHANGE_URL = os.getenv("EXCHANGE_URL", "https://inception.dachain.io/exchange")
CRATE_URL = os.getenv("CRATE_URL", "https://inception.dachain.io/quantum-crate")

EXTENSION_DIR = os.path.abspath(
    os.getenv("EXTENSION_DIR", "./metamask-extension")
)

USER_DATA_DIR = os.path.abspath(
    os.getenv("USER_DATA_DIR", "./pw-profile")
)

CDP_PORT = int(os.getenv("CDP_PORT", "9222"))
DISPLAY = os.getenv("DISPLAY", ":99")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"