import os
import time
from dotenv import load_dotenv
from utils.custom_logger import log
from pymongo import MongoClient, ASCENDING, DESCENDING
load_dotenv()

class MongoDBService:
    def insert_chat(self,**kwargs):
        try:
            start_time = time.time()
            con=os.getenv("MONGODB")
            with MongoClient(con) as client:
                client["UETGPT"]["chats"].insert_one(kwargs)
            log.warning(f"Time taken for insert_chat: {round(time.time() - start_time,2)}")
        except Exception as e:
            log.error(f"Error in insert_chat: {e}", exc_info=True)
            return "Sorry, I am unable to process your request at the moment. Please try again later."


    def fetch_chats(self,userid:str):
        try:
            start_time = time.time()
            con=os.getenv("MONGODB")
            with MongoClient(con) as client:
                cursor= client["UETGPT"]["chats"].find({"userid":userid}).sort("created_at",DESCENDING).limit(6)
                chats= list(cursor)
                log.warning(f"Time taken for fetch_chats: {round(time.time() - start_time,2)}")
                return(chats)
        except Exception as e:
            log.error(f"Error in fetch_chats: {e}", exc_info=True)
            return "Sorry, I am unable to process your request at the moment. Please try again later."
        