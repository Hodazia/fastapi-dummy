from fastapi import FastAPI, Request, Header, HTTPException
from config import GITHUB_WEBHOOK_SECRET
import uvicorn
import hashlib
import hmac
from config import GITHUB_WEBHOOK_SECRET
import json



'''
I will be coding a github webhook receive service,

- so whatever changes in a github account , be it commits,PR, issues or anything else
- that changes has to be sent as A post request to /api/webhooks and received in this backend
- and then this backend does some sort of service

HOW GITHUB CREATES THE SIGNATURE
Assume secret : my_secret_key
Payload : {  "message" : "hello" }
Github computes,
 HMAC_SHA256(
    secret="my_super_secret_key",
    message='{"message":"hello"}'
)

Result as , 9af8b2c7...
Github adds this to the request headers
X-Hub-Signature-256:sha256=9af8b2c7...

HOW TO SETUP, 
first clone the repo, create a .env file, then create webhooks on your github repo, and make sure to make
Content-type as application/json and add the same env variables value,  too as secret
1. run the main.py using python main.py
2. in the another terminal make sure to run ngrok using, `ngrok http 8000`
3. and then u can make changes to the github and that will be seen in the logs of the endpoint,


'''



app = FastAPI()
@app.on_event("startup")
async def startup():
    print("SECRET:", GITHUB_WEBHOOK_SECRET)

def verify_signature(payload_body: bytes, signature_header: str):
    """
    Verify GitHub webhook signature, 
    """

    if not signature_header:
        raise HTTPException(
            status_code=401,
            detail="Missing signature"
        )

    # create our own signature 
    hash_object = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256
    )

    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(
        expected_signature,
        signature_header
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid signature"
        )

@app.post("/github/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):

    body = await request.body()
    # this body will be in raw bytes bytes,it contains the event data, b'{"ref":"refs/heads/main",...}'

    # check what is sent in the body as well,
    # print("The body sent is ", body)
    # print("="*80)
    # print("The signature is ", x_hub_signature_256)
    # print("="*80)
    verify_signature(
        body,
        x_hub_signature_256
    )

    # print("BODY RAW:", body)
    # print("BODY LENGTH:", len(body))
    payload = json.loads(body)

    print("=" * 80)
    print(f"EVENT TYPE : {x_github_event}")
    print(json.dumps(payload, indent=2))
    print("=" * 80)

    return {
        "status": "success",
        "event": x_github_event
    }


@app.get("/")
def main():
    return {
        "message":"hello from microservice-1"
    }

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8000)

