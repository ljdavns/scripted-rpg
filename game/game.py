from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))
import config
from enum import Enum
from prompt.prompt import GameStages, RpgPrompt
from game.story import Story
from bot.bot import bot_generate, reset_chat_history, get_chat_history
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage
)

class Game:

    id: str = 'default_game'
    current_stage: GameStages = GameStages.INTRO
    story: Story = None
    story_started: bool = False
    bot_callback = None

    def __init__(self, story: Story, bot_callback):
        self.story = story
        self.bot_callback = bot_callback

    def start(self):
        return self.update()

    def update(self, player_input: str = None):
        update_stage = True
        if self.current_stage == GameStages.INTRO:
            prompt = RpgPrompt.BASE_PROMPT.value + RpgPrompt.INTRO_PROMPT.value.format(self.story.intro)
            result = self.bot_callback(game_id=self.id, message=prompt, message_type='system')
        elif self.current_stage == GameStages.STORY:
            result, story_end = self.story_loop(player_input)
            update_stage = story_end
        elif self.current_stage == GameStages.ANALYZE:
            prompt = RpgPrompt.ANALYZE_PROMPT.value.format(self.story.reveal)   
            result = self.bot_callback(game_id=self.id, message=prompt, message_type='system')
        elif self.current_stage == GameStages.REVEAL:
            prompt = RpgPrompt.REVEAL_PROMPT.value.format(self.story.reveal)
            result = self.bot_callback(game_id=self.id, message=prompt, message_type='system')
        if update_stage:
            if self.current_stage == GameStages.REVEAL:
                return result + 'THE END\n'
            self.current_stage = GameStages.get_list()[GameStages.get_list().index(self.current_stage) + 1]
        return result

    def story_loop(self, player_input):
        result = ''
        chapter_end = False
        story_end = False
        if (not self.story_started):
            # system_prompt = RpgPrompt.STORY_START_PROMPT.value.format(player_input, 1, self.story.get_current_chapter())
            # chat_history = get_chat_history(self.id)
            # chat_history += [SystemMessage(content=system_prompt)]
            # result = bot_generate(self.id, self.story.get_current_plot(), message_type='AI', chat_history=chat_history)
            # # result = bot_generate(self.id, system_prompt, message_type='system', chat_history=chat_history)
            prompt = RpgPrompt.PLOT_UPDATE_PROMPT.value.format('select character' + player_input, self.story.get_current_plot())
            result = self.bot_callback(game_id=self.id, message=prompt, message_type='system')
            self.story_started = True
        else:
            next_plot, chapter_end, story_end = self.story.update()
            # chat_history = get_chat_history(self.id)
            # chat_history.append(HumanMessage(content=player_input))
            prompt = RpgPrompt.PLOT_UPDATE_PROMPT.value.format(player_input, next_plot) if (not story_end) else RpgPrompt.PLOT_UPDATE_END_PROMPT.value.format(player_input, next_plot)
            result = self.bot_callback(game_id=self.id, message=prompt, message_type='system')
            # result = bot_generate(self.id, player_input, message_type='human')
        if (chapter_end and (not story_end)):
            summarized_result = self.bot_callback(game_id=self.id, message=RpgPrompt.SUMMARIZE_CHAPTER_PROMPT.value, message_type='system')
            chat_history = get_chat_history(self.id)
            new_chat_history = chat_history[:2] + chat_history[-4:-2] + \
                [SystemMessage(content=RpgPrompt.PREVIOUS_SUMMARIZED_CHAPTERS_PROMPT.value.format(summarized_result))]
            reset_chat_history(self.id, new_chat_history)
            # new_message = SystemMessage(content=RpgPrompt.CHAPTER_START_PROMPT.value.format(self.story.current_chapter_index+1, summarize_result, self.story.get_current_chapter()))
            # result = bot_generate(self.id, new_message, message_type='system', chat_history=new_chat_history)
        # if ('章节结束' in result):
        #     story_end = self.story.update_chapter()
        #     if (not story_end):
        #         summarize_result = bot_generate(self.id, RpgPrompt.SUMMARIZE_CHAPTER_PROMPT, message_type='system')
        #         chat_history = get_chat_history(self.id)
        #         new_chat_history = chat_history[:5]
        #         clear_chat_history(self.id)
        #         new_message = SystemMessage(content=RpgPrompt.CHAPTER_START_PROMPT.value.format(self.story.current_chapter_index+1, summarize_result, self.story.get_current_chapter()))
        #         result = bot_generate(self.id, new_message, message_type='system', chat_history=new_chat_history)
        return result, story_end


if __name__ == "__main__":
    story = Story('the_rats_in_the_walls')
    print(story.intro)
    game = Game(story, bot_generate)
    print(game.start())
    while True:
        player_input = input()
        print(game.update(player_input))
