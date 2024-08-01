from services.chroma_service import *
from services.openai_service import *
from services.mongodb_service import *
from utils.custom_logger import log
from prompts.uet_prompt import *
import gradio as gr
import datetime

class PropertyBotService:
    def __init__(self,userid:str):
        self.userid = userid
        self.chromadb_service = ChromaService()
        self.openai_service = OpenAIService()
        self.mongodb_service = MongoDBService()

    def ask(self,question:str):

        # Insert user question into MongoDB database
        try:
            self.mongodb_service.insert_chat(
                userid=self.userid,
                role="user",
                msg=question,
                created_at=datetime.datetime.now()
            )
        except Exception as e:
            log.error(f"Error in insert_chat: {e}", exc_info=True)


        # Retrieve documents from the Chroma VectorDatabase
        docs = self.chromadb_service.retriver(question)
        
        # Prepare Dynamic Prompt with the Data from VectorDatabase
        DOC_PROMPT = 'This is from where you can possibly get information about the user question'
        for doc in docs:
            DOC_PROMPT += "\n" + doc
        messages = [
            {
                "role": "system",
                "content": UET_PROMPT
            },
            {
                "role": "system",
                "content": DOC_PROMPT
            },
        ]

        # Fetch previous chats from the MongoDB database
        try:
            chats = self.mongodb_service.fetch_chats(self.userid)
            for chat in chats:
                    # Append the previous chats to the messages list just like OpenAI format
                    messages.append(
                    {
                        "role":chat['role'],
                        "content":chat["msg"]
                    }
                    )
        except Exception as e:
            log.error(f"Error in fetch_chats: {e}", exc_info=True)
        
        # Append the user question to the messages list just like OpenAI format
        messages.append({"role":"user","content":question})

        # Get response from OpenAI
        response,response_object = self.openai_service.askai(messages)

        # Insert the response into MongoDB database
        try:
            self.mongodb_service.insert_chat(
                userid=self.userid,
                role="assistant",
                msg=response,
                response_object=self.openai_service.get_response_dict(response_object),
                created_at=datetime.datetime.now()
            )
        except Exception as e:
            log.error(f"Error in insert_chat: {e}", exc_info=True)
        return response

    def interface(self,share:bool=False):
        with gr.Blocks(title="UETGPT Demo Interface") as demo:
                gr.Markdown("## UETGPT Demo Interface")
                
                with gr.Row():
                    gr.Markdown("")
                    with gr.Column(scale=6):
                        chatbot = gr.Chatbot()
                        with gr.Row():    
                            msg = gr.Textbox(scale=9,container=False)
                            btn = gr.Button(value='submit', variant='primary')
                            clear = gr.ClearButton([msg, chatbot])
                    gr.Markdown("")
                    

                def respond(message, history):
                    if message == '':
                        resp_message = "Please Enter a valid question"
                        history = history + [[message,'']]
                    else:
                        history = history + [[message,'']]
                        resp_message = self.ask(message)
                    
                    for i in resp_message:
                        history[-1][1] += i
                        yield "",history

                msg.submit(respond, [msg, chatbot], [msg, chatbot])
                btn.click(respond, [msg, chatbot], [msg, chatbot])

        demo.queue()
        a,b,c = demo.launch(
        prevent_thread_lock = True,
        share = share
        
        )
        return b,c
