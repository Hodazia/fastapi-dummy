''' store the github webhook secrets that the Github will send as well as we will have it 
in the .env file which we will use to verify the signature,
else anyone with the github webhook endpoint can send a message to me, 
 
 
  '''

from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
