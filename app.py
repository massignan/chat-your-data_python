import os
from typing import Optional, Tuple

import gradio as gr
from query_data import get_chain
from threading import Lock
import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = Pinecone.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embeddings)

def set_openai_api_key(api_key: str):
    '''Set the API key and return chain.
       If no api_keym the None is returned.'''
    
    if api_key:
        os.environ["OPENAI_API_KEY"] =  api_key
        chain = get_chain(vectorstore)
        os.environ["OPENAI_API_KEY"] = ""
        return chain

chain = set_openai_api_key(OPENAI_API_KEY)

class ChatWrapper:

    def __init__(self) -> None:
        self.lock = Lock()
    def __call__(self, inp: str, history: Optional[Tuple[str, str]]) :
        self.lock.acquire()
        try:
            history = history or []
            # If chain is None, that is because no API key was provided.
            if chain is None:
                history.append((inp, "OpenAI key was not loaded!"))
                return history, history
            # Set OpenAI key
            import openai
            openai.api_key = OPENAI_API_KEY #api_key
            # Run chain and append input.
            output = chain({"question": inp, "chat_history": history})["answer"]
            history.append((inp, output))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history, history
    
chat = ChatWrapper()

block = gr.Blocks(css=".gradio-container {background-color: lightgray}")

with block:
    with gr.Row():
        gr.Markdown("<h3><center>Chat-Your-Data</center></h3>")

        chatbot = gr.Chatbot()

    with gr.Row():
        message = gr.Textbox(
            label="What's your question?",
            placeholder="Ask your questions here.",
            lines=1,
        )
        submit = gr.Button(value="Send", variant="secondary").style(full_width=False)

    gr.Examples(
        examples=[
            "In what ways has the Ukraine conflict affected the global economy?",
            "Summarize the state of the global economy in 2022, taking into account its GDP performance."
        ],
        inputs=message,
    )

    gr.HTML(
        "<center>Powered by João Paulo Druzina Massignan</a></center>"
    )

    state = gr.State()
    agent_state = gr.State()

    submit.click(chat, inputs=[message, state], outputs=[chatbot, state])
    message.submit(chat, inputs=[message, state], outputs=[chatbot, state])

block.launch(debug=True)