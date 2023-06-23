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

from bot.bot import bot_generate_stream, bot_generate
from game.story import Story
from game.game import Game
from pydantic import BaseModel
from prompt.prompt import RpgPrompt

app = FastAPI(
    title="Langchain AI API",
)

story = Story('the_rats_in_the_walls')
print(story.intro)
game = Game(story, bot_generate_stream)

@app.on_event("startup")
async def startup():
    print("Server Startup!")

@app.post("/get-intro")
def start():
    return game.get_intro()

class Command(BaseModel):
    message: str

@app.post("/bot")
async def stream(command: Command):
    return StreamingResponse(game.update(command.message), media_type='text/event-stream')

@app.post("/get-image-prompt")
def get_image_prompt(command: Command):
    return bot_generate(game_id='default_game', message=RpgPrompt.IMAGE_PROMPT.value.format(command.message), history_enabled=False, message_type='system')

from pathlib import Path
from fastapi.responses import HTMLResponse
@app.get("/")
def read_root():
    html_content = Path(config.PROJECT_BASE_DIR + '/frontend/simple.html').read_text()
    return HTMLResponse(content=html_content)

uvicorn.run(app, host="0.0.0.0", port=8000)
