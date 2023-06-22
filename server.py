import config
import set_keys
import threading
import queue

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


app = FastAPI(
    title="Langchain AI API",
)


@app.on_event("startup")
async def startup():
    print("Server Startup!")

class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)

def llm_thread(g, prompt):
    try:
        chat = ChatOpenAI(
            verbose=True,
            streaming=True,
            callback_manager=BaseCallbackManager([ChainStreamHandler(g)]),
        )
        chat([SystemMessage(content="You are a poetic assistant"), HumanMessage(content=prompt)])

    finally:
        g.close()


def chat(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g


@app.post("/bot")
async def stream():
    return StreamingResponse(chat("Write me a song about sparkling water."), media_type='text/event-stream')

from pathlib import Path
from fastapi.responses import HTMLResponse
@app.get("/")
def read_root():
    html_content = Path(config.PROJECT_BASE_DIR + '/frontend/simple.html').read_text()
    return HTMLResponse(content=html_content)

uvicorn.run(app, host="0.0.0.0", port=8000)
