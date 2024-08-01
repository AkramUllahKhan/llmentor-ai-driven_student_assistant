import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from utils.custom_logger import *
load_dotenv()

class OpenAIService:
    def askai(self,messages:list):
        try:
            start_time = time.time()
            client = OpenAI()
            response = client.chat.completions.create(
            temperature=0,
            model=os.getenv("MODEL", "gpt-4o"),
            messages=messages
            )
            log.warning(f"Time taken for AskAI: {round(time.time() - start_time,2)}")
            return response.choices[0].message.content,response
        except Exception as e:
            log.error(f"Error in AskAI: {e}", exc_info=True)
            return "Sorry, I am unable to process your request at the moment. Please try again later.",None

    def get_response_dict(self,response:dict):
        try:
            response.choices[0].message = None
            response.choices = vars(response.choices[0])
            response.usage = vars(response.usage)
            response = vars(response)
            return response
        except Exception as e:
            log.error(f"Warning in get_response_dict: {str(e)}", exc_info=True)
            return None