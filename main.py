from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.uetbot_service import PropertyBotService

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demonstration purposes
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask(input_data:dict = {
    "userid": "akram@gmail.com",
    "question": "Hi UET stads for.? "
   }):
    try:
        propertybot_service = PropertyBotService(userid=input_data.get('userid'))
        response = propertybot_service.ask(question=input_data.get("question"))
        return {"response":response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interface")
async def interface(
    input_data:dict = {
    "userid": "akram@gmail.com",
    "share": False
   }):
    try:
        propertybot_service = PropertyBotService(userid=input_data.get('userid'))
        Local_Link,Public_Link = propertybot_service.interface(share=input_data.get("share",False))
        return {"local": Local_Link, "public": Public_Link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
