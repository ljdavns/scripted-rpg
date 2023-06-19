from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))
import config
from enum import Enum

class GameStages(Enum):
    INTRO = {
        "name": "intro",
        # "goal": "Give the player the story's background and beginning, and list all the charaters and their roles in the story,then ask the player to select a character.",
        "goal": "Ask the player to select a character.",
    }
    STORY = {
        "name": "story",
        "goal": "Update the story to the later plot based on the action's effect and the storybook."
    }
    ANALYZE = {
        "name": "analyze",
        "goal": "Tell the player the story's ending and ask some vital questions based on the [hidden truth]."
    }
    REVEAL = {
        "name": "reveal",
        "goal": "List the above vital questions and their answers, and tell the player the [hidden truth]."
    }
    
    @staticmethod
    def get_list():
        return [stage for stage in GameStages]

    @staticmethod
    def get_key_list():
        return [stage.value["name"] for stage in GameStages]

    @staticmethod
    def get_json_str_list():
        return [str(stage.value) for stage in GameStages]
    
    @staticmethod
    def get_all_items_as_json_str():
        result = {}
        for stage in GameStages:
            result[stage.name] = stage.value
        return str(result)

class RpgPrompt(Enum):

    BASE_PROMPT: str = "Now you are given a [storybook] to read and update the story plot and game process, \
        which contains the whole story and the [hidden truth] about the story. \
        The game is divided into these processes: {}. \
        The story plot updates should be minimal based on the player's action. \
        Note that this story is designed with a predetermined plot and conclusion. The choices made by the user will not alter the final direction and outcome of the plot. The user's choices will only affect the status and experiences of the character they play throughout the story. \
        To achieve this, you need to guide the plot back to the original main storyline after each user's choice, without deviating from the overall designed story framework. Some methods that can be adopted include: \
        1. Setting key plot event points. No matter how the user chooses, certain plot progressions occur at these key event points, guiding the story back to the mainline. \
        2. For each user choice, assign corresponding outcomes and subsequent plots. However, these different branch plots will eventually converge at the same node, and then continue the original mainline. \
        3. Integrate some inconsequential choices into the user's selection options. The results of these choices will not affect the subsequent main plot and will only create minor episodes \
            but will eventually return to the mainline. This gives the user a sense of choice, but the result of the choice does not alter the direction of the story. \
        4. Allow some of the user's choices to have certain effects, but these effects only manifest in changes to the user's character status and do not alter the progression of other characters and events in the story. \
            The challenges faced by the user character may change, but the original story must still continue. \
        5. Reasonably arrange for plot events that the user cannot choose or control, so that you can guide the story back to your established framework at any time. \
            The user only controls their character's choices, but cannot control all changes in the entire story world.".format(GameStages.get_json_str_list())

    GET_INTRO_PROMPT: str = "What's the story's background and beginning based on the storybook?"
    INTRO_PROMPT: str = "The story's background and the beginning is: `{{}}` \
        Now {}".format(GameStages.INTRO.value["goal"])
    
    STORY_START_PROMPT: str = "The player has selected a character `{}`. Now the story has started in `chapter{}`, this chapter's [storybook] is `{}`. \
        Please update the story plot by the background and beginning and the [storybook], then give the player a list of actions to take."
    CHAPTER_START_PROMPT: str = "Now the story is in `chapter{}`, the previous plot summarized is `{}`, this chapter's [storybook] is `{}`. \
        Please update the story plot by the previous summarization and beginning and the [storybook], then give the player a list of actions to take."
    PLOT_UPDATE_PROMPT: str = "The player has made an action `{}`. \
        If the player's action leads to this chapter's end, print `chapter end` at your response end \
        else update the story to the later plot based on the action's effect and the storybook. \
        After updating the plot, give the player related to current plot a new list of actions based on the new plot for them to take."
    SUMMARIZE_CHAPTER_PROMPT: str = "Now this chapter is end, please summarize all the story's plot so far."
    
    ANALYZE_PROMPT: str = "Now the story ends, and the [hidden truth] are `{{}}`. You should {}".format(GameStages.ANALYZE.value["goal"])

    REVEAL_PROMPT: str = "Now the player has made the answers. You should {}".format(GameStages.REVEAL.value["goal"])

if __name__ == "__main__":
    print(GameStages.get_all_items_as_json_str())
    print(RpgPrompt.BASE_PROMPT.value)
    print(RpgPrompt.INTRO_PROMPT.value.format('sss'))