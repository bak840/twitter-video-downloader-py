import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'CONSUMER_KEY': os.getenv('CONSUMER_KEY'),
    'CONSUMER_SECRET': os.getenv('CONSUMER_SECRET'),
    'ACCESS_TOKEN_KEY': os.getenv('ACCESS_TOKEN_KEY'),
    'ACCESS_TOKEN_SECRET': os.getenv('ACCESS_TOKEN_KEY')
}
