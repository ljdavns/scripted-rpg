from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))
import config
from prompt.prompt import RpgPrompt
from bot.bot import bot_generate

class Story:

    background: str = ''
    story_name: str = ''
    story_path: str = ''
    intro: str = ''
    reveal: str = ''
    chapters: list = []
    current_chapter_index: int = 0
    current_plots: list = []
    current_plot_index: int = 0

    def __init__(self, story_name):
        self.story_path = config.DOC_PATH + '/' + story_name
        self.story_name = story_name
        self.intro = self._get_intro()
        self.reveal = self._get_reveal()
        self.chapters = self._get_chapters()
        self.current_plots = self._get_current_plots()
        # test
        self.current_chapter_index = 3
        self.current_plot_index = 0

    def _get_intro(self):
        intro_path = self.story_path + '/intro.txt'
        with open(intro_path, 'r') as f:
            intro = f.read()
        return intro

    def _get_reveal(self):
        reveal_path = self.story_path + '/reveal.txt'
        with open(reveal_path, 'r') as f:
            reveal = f.read()
        return reveal
    
    def _get_chapters(self):
        chapters_path = self.story_path + '/chapters.md'
        with open(chapters_path, 'r') as f:
            chapters_str = f.read()
        chapters = list(map(lambda chapter: chapter, chapters_str.split('CHAPTER END  \n')[:-1]))
        return chapters
    
    def _get_current_plots(self):
        self.current_plot_index = 0
        return self.chapters[self.current_chapter_index].split('\n')[1:-1]
    
    def _update_plot(self):
        self.current_plot_index += 1
        if self.current_plot_index >= len(self.current_plots):
            return True
        return False

    def _update_chapter(self):
        self.current_chapter_index += 1
        if self.current_chapter_index >= len(self.chapters):
            return True
        self.current_plots = self._get_current_plots()
        return False
    
    def update(self):
        chapter_end = self._update_plot()
        story_end = False
        if chapter_end:
            story_end = self._update_chapter()
        return self.current_plots[self.current_plot_index], chapter_end, story_end

    def get_current_chapter(self):
        return self.chapters[self.current_chapter_index]
    
    def get_current_plot(self):
        return self.current_plots[self.current_plot_index]

    def summarize_current_chapter(self):
        pass

    def end(self):
        pass
   

if __name__ == "__main__":
    story = Story('the_rats_in_the_walls')
    pass