import os
from dotenv import load_dotenv

load_dotenv()
HOME_REPO = os.path.abspath(os.path.dirname(__file__) + '/..')
TEMP_FOLDER = '/tmp/dgpt'
os.makedirs(TEMP_FOLDER, exist_ok=True)

API_KEY = os.environ.get('API_KEY')
MAX_TOKENS = os.environ.get('MAX_TOKENS')
NUM_WORDS = os.environ.get('NUM_WORDS')
APP_PORT = int(os.environ.get('APP_PORT'))
