'''
- basically here u can create variables to load all your environment variables

'''

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")