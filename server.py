import config
import set_keys_local

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from bot.bot import bot_generate_stream, bot_generate
from game.story import Story
from game.game import Game
from pydantic import BaseModel
from prompt.prompt import RpgPrompt
import io

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

import time
def slow_string_generator(input_str: str):
    time.sleep(1)
    for char in input_str:
        time.sleep(0.02)
        if (char == '\n'):
            time.sleep(0.2)
        yield char

import re
def html_tag_generator(input_str: str):
    tag_pattern = re.compile(r'<[^>]*?>.*?</[^>]*?>')
    time.sleep(0.5)

    last_index = 0
    for match in tag_pattern.finditer(input_str):
        # Yield non-HTML content one character at a time
        for char in input_str[last_index:match.start()]:
            time.sleep(0.08)
            yield char
        
        # Yield the entire HTML tag at once
        time.sleep(1)
        yield match.group()
        last_index = match.end()

    # Yield remaining non-HTML content
    for char in input_str[last_index:]:
        time.sleep(0.08)
        yield char

@app.post("/bot")
async def stream(command: Command):
    result = game.update(command.message)
    # return StreamingResponse(slow_string_generator('66666666666666666666666666666'), media_type='text/event-stream')
    return StreamingResponse(html_tag_generator(result) if type(result) == str else result, media_type='text/event-stream')

@app.post("/get-image-prompt")
def get_image_prompt(command: Command):
    return bot_generate(game_id='default_game', message=RpgPrompt.IMAGE_PROMPT.value.format(command.message), history_enabled=False, message_type='system')

from pathlib import Path
from fastapi.responses import HTMLResponse
@app.get("/")
def read_root():
    html_content = Path(config.PROJECT_BASE_DIR + '/frontend/simple.html').read_text()
    return HTMLResponse(content=html_content)

# launch server
uvicorn.run(app, host="0.0.0.0", port=8080)
import webbrowser
webbrowser.open('http://localhost:8080', new=2)
