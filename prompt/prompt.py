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
        "goal": "Ask players some questions about the core story."
    }
    REVEAL = {
        "name": "reveal",
        "goal": "Output the reveal to players."
    }
    END = {
        "name": "the end",
        "goal": "the end"
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

    # BASE_PROMPT: str = "Now you are given a [storybook] to read and update the story plot and game process, \
    #     which contains the whole story and the [hidden truth] about the story. \
    #     The game is divided into these processes: {}. \
    #     The story plot updates should be minimal based on the player's action. \
    #     Note that this story is designed with a predetermined plot and conclusion. The choices made by the user will not alter the final direction and outcome of the plot. The user's choices will only affect the status and experiences of the character they play throughout the story. \
    #     To achieve this, you need to guide the plot back to the original main storyline after each user's choice, without deviating from the overall designed story framework. Some methods that can be adopted include: \
    #     1. Setting key plot event points. No matter how the user chooses, certain plot progressions occur at these key event points, guiding the story back to the mainline. \
    #     2. For each user choice, assign corresponding outcomes and subsequent plots. However, these different branch plots will eventually converge at the same node, and then continue the original mainline. \
    #     3. Integrate some inconsequential choices into the user's selection options. The results of these choices will not affect the subsequent main plot and will only create minor episodes \
    #         but will eventually return to the mainline. This gives the user a sense of choice, but the result of the choice does not alter the direction of the story. \
    #     4. Allow some of the user's choices to have certain effects, but these effects only manifest in changes to the user's character status and do not alter the progression of other characters and events in the story. \
    #         The challenges faced by the user character may change, but the original story must still continue. \
    #     5. Reasonably arrange for plot events that the user cannot choose or control, so that you can guide the story back to your established framework at any time. \
    #         The user only controls their character's choices, but cannot control all changes in the entire story world.".format(GameStages.get_json_str_list())

    BASE_PROMPT: str = "Now you are given [later plot] to update the story plot and game process \
        Note that this story is designed with a predetermined plot and conclusion, So regardless of the choices the player has chosen previously, \
        connect the predetermined subsequent story line and the player's earlier selections in a coherent fashion.\
        For example: [previous plot]: I saw a bird stood on the window. [action]: open the light. [later plot]:The bird flew away to the underbase.\
        [updated plot]: I opened the light then the bird got freak out, then the bird flew away to the underbase.".format(GameStages.get_json_str_list())

    GET_INTRO_PROMPT: str = "What's the story's background and beginning based on the storybook?"
    INTRO_PROMPT: str = "The story's background and the beginning is: `{{}}` \
        Now {}".format(GameStages.INTRO.value["goal"])
    
    STORY_START_PROMPT: str = "The player has selected a character `{}`. Now the story has started in `chapter{}`, this chapter's [storybook] is `{}`. \
        Please update the story plot by the background and beginning and the [storybook], then give the player a list of actions to take(and also others for user to input)."
    CHAPTER_START_PROMPT: str = "Now the story is in `chapter{}`, the previous plot summarized is `{}`, this chapter's [storybook] is `{}`. \
        Please update the story plot by the previous summarization and beginning and the [storybook], then let the players input custom action.\
        Output the next paragraph from the original [storybook] each time as the new plot."
    # PLOT_UPDATE_PROMPT: str = "The player has made an action `{}`. \
    #     If the player's action leads to this chapter's end, print `chapter end` at your response end \
    #     else update the story to the later plot based on the action's effect and the storybook. \
    #     After updating the plot, give the player related to current plot a new list of actions based on the new plot(the next paragraph) for them to take(and also others for user to input)."
    PLOT_UPDATE_PROMPT: str = "The player has made an [action] `{}`. \
        Please update the story to the [later plot] of `{}`, and produce an opening passage of players' action to the new plot before transitioning into the next fixed storyline. \
        After updating the plot, give the players a list of actions to chose or input their custom action."
    PLOT_UPDATE_END_PROMPT: str = "The player has made an [action] `{}`. \
        Please update the story to the [later plot] of `{}`, and produce an opening passage of players' action to the new plot before transitioning into the next fixed storyline. \
        Then just output only the storyline to user, do not output the notice to let the player input action."
    SUMMARIZE_CHAPTER_PROMPT: str = "Now this chapter is end, please summarize all the stories of the post chapters after the players pick characters."
    PREVIOUS_SUMMARIZED_CHAPTERS_PROMPT: str = "The previous chapters' summarized stories are: `{}`."

    IMAGE_PROMPT: str = "Please summarize this sentence `{}` and output it in English."

    ANALYZE_PROMPT: str = "Now the story ends, you should {} and do not edit the question.The questions are: {{}}".format(GameStages.ANALYZE.value["goal"])

    REVEAL_PROMPT: str = "Now the player has made the answers. You should {} and do not edit the reveal.The reveal is: {{}}".format(GameStages.REVEAL.value["goal"])

if __name__ == "__main__":
    print(GameStages.get_all_items_as_json_str())
    print(RpgPrompt.BASE_PROMPT.value)
    print(RpgPrompt.INTRO_PROMPT.value.format('sss'))