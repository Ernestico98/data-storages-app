from dotenv import load_dotenv
load_dotenv()

from manager.connection import connect
from manager.setup_models import setup_models

if __name__ == "__main__":
    setup_models()
