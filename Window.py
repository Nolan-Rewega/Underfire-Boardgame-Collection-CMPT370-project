import pygame as pg
from ConnectFour import ConnectFour
from MainMenu import MainMenu
from OptionMenu import OptionMenu
from Profile import Profile
from LoadingScreen import LoadingScreen
from Button import button
from Slider import slider
from DropBox import dropBox
from Database import Database
from Leaderboard import Leaderboard
class Window:

    def __init__(self):
        """
        Window's constructor class
        """
        # initialize pygame
        pg.init()

        # make variable for database calls
        self.db = Database()

        # Get settings from database as a dictionary
        self.settings_dic = self.db.get_settings()

        # sounds
        self.BG_TRACK = "Assets/Simian Segue - Donkey Kong Country.mp3"
        self.music_vol = self.settings_dic["music"] / 100
        self.SFX_vol = self.settings_dic["sound"] / 100

        # initialize displaying flags
        self.running = True
        self.playing = False

        # game difficulty setting
        self.difficulty = self.settings_dic["difficulty"]

        # initialize key flags
        self.ENTER_KEY, self.BACKSPACE_KEY, self.ESCAPE_KEY = False, False, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False

        # initialize mouse flags and objects
        self.mx, self.my = 0, 0
        self.LEFT_CLICK = False
        self.RIGHT_CLICK = False

        # initialize display settings
        self.DISPLAY_W, self.DISPLAY_H = self.settings_dic["res_width"], self.settings_dic["res_height"]
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        pg.display.set_caption("UnderFire's Board Game Collection")
        self.logo = pg.image.load('Assets/UnderFireLogo.png').convert_alpha()
        pg.display.set_icon(self.logo)

        # initialize font, color pallet, decor ..etc
        self.font = pg.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        # initialize menu, game, and database objects
        self.main_menu = MainMenu(self)
        self.options_menu = OptionMenu(self)
        self.profile = Profile(self)
        self.Leaderboard = Leaderboard(self)

        self.current_screen = LoadingScreen(self)

    def play_music(self):
        """
        play's the background music
        :return: None
        """
        pg.mixer.music.load(self.BG_TRACK)
        pg.mixer.music.set_volume(self.music_vol)
        pg.mixer.music.play(-1)

    def change_music_vol(self):
        """
        changes the volumne of the current music track playing
        :return: None
        """
        pg.mixer.music.set_volume(self.music_vol)

    def play_sound(self, sound_path):
        """
        play a given sound EG: sound_path = "Assets/Simian Segue - Donkey Kong Country.mp3"
        :param sound_path: A string Representing the File Path from the working directory
        :return: None
        """
        sound = pg.mixer.Sound(sound_path)
        # play the sound at the given SFX_vol
        sound.set_volume(self.SFX_vol)
        sound.play()

    def mute_music(self):
        pass

    # checks for player input
    def set_user_input(self):
        """
        get the user input from pygame's event listener and saves
        it to the corresponding key or mouse flag.
        :return: None
        """
        # get mouse position
        self.mx, self.my = pg.mouse.get_pos()

        for event in pg.event.get():
            # check if player has quit ("clicked X on window")
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
                # set the Main menus display variable to false
                self.current_screen.is_displaying = False

            # check if the player has clicked the mouse
            if event.type == pg.MOUSEBUTTONDOWN:
                # button "1" = left click
                # button "2" = right click
                if event.button == 1:
                    self.LEFT_CLICK = True
                if event.button == 3:
                    self.RIGHT_CLICK = True

            # check for key presses
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pg.K_ESCAPE:
                    self.ESCAPE_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACKSPACE_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pg.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_key_inputs(self):
        """
        resets all the flags to False
        :return: None
        """
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False
        self.BACKSPACE_KEY, self.ENTER_KEY, self.ESCAPE_KEY = False, False, False
        self.LEFT_CLICK, self.RIGHT_CLICK = False, False

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        """
        draws text onto the screen with the provided values
        :param text: a string representing the text to display
        :param size: a integer representing the size of the text
        :param x: a integer representing the x coordinate to display the text at
        :param y: a integer representing the y coordinate to display the text at
        :param color: a Triple of ints, representing (R,G,B) values.
        :return: None
        """
        # everything uses default font for now will change for later.
        font = pg.font.Font(self.font, size)
        text_surface = font.render(text, True, color)

        # create a rectangle object and put text inside
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x, y)

        # blit the text
        self.display.blit(text_surface, text_rectangle)

    def draw_textwrapped(self, x, y, w, h, text, size, color=(255, 255, 255), aa=False, bkg=None):
        """
        Wraps text in box and displays it.
        https://www.pygame.org/wiki/TextWrap,
        provided code from pygame wiki modified.
        :param text: A string representing the text to display
        :param color: A Triple (R,G,B) of Ints representing the color of the text
        :param x: A integer representing the x cord of the rectangle
        :param y: A integer representing the y cord of the rectangle
        :param w: A integer representing the width of the rectangle
        :param h: A integer representing the height of the rectangle
        :param size: A integer representing size of the font
        :param aa: ??? Boolean
        :param bkg: ??? IMG file path?
        :return: None
        """

        font = pg.font.Font(self.font, size)
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > y+h:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < w and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], True, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            self.display.blit(image, (x, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

    def draw_rect(self, color, x, y, width, height):
        """
        draws a rectangle onto the screen with the provided values
        :param color: a Triple "(R,G,B)" of integers that represent RGB value.
        :param x: a integer representing the starting x coordinate to display the text at
        :param y: a integer representing the starting y coordinate to display the text at
        :param width: a integer representing the width of the box
        :param height: a integer representing the height of the box
        :return: none
        """
        # create the rectangle of size (width, height)
        # of color (R,G,B)
        rectangle_surf = pg.Surface((width, height))
        rectangle_surf.fill(color)

        # blit the rectangle at (x,y)
        self.display.blit(rectangle_surf, (x, y))

    def draw_image(self, filepath, x, y, width, height):
        """
        draws an image onto the screen with the provided values
        :param filepath: a String representing the file path of the image
        :param x: a integer representing the starting x coordinate to display the image at
        :param y: a integer representing the starting y coordinate to display the image at
        :param width: a integer representing the width of the image
        :param height: a integer representing the height of the image
        :return: None
        """
        image = pg.image.load(filepath).convert_alpha()
        # transform the image width and height to ones given
        imgTransform = pg.transform.scale(image, (width, height))

        # blit the image at (x,y)
        self.display.blit(imgTransform, (x, y))

    def create_button(self, x, y, width, height, buttonColours, textColours, text=None, image=None):
        """
        creates an button with the provided values
        :param x: a integer representing the starting x coordinate to display the button at
        :param y: a integer representing the starting y coordinate to display the button at
        :param width: a integer representing the width of the button
        :param height: a integer representing the height of the button
        :param buttonColours: a Triple of ints, representing (R,G,B) values.
        :param textColours: a Triple of ints, representing (R,G,B) values.
        :param text: a string representing the text to display (optional)
        :param image: a image representing the image to display (optional)
        :return: A button class
        """
        font = pg.font.Font(self.font, int(width))
        # Create the button
        if text is not None:
            return button(self.display, x, y, width, height, buttonColours, textColours, font, text)
        if image is not None:
            return button(self.display, x, y, width, height, buttonColours, textColours, font, image)

    def create_slider(self, x, y, width, height, percentage):
        """
        creates an slider with the provided values
        :param x: the x coordinate of the slider
        :param y: the y coordinate of the slider
        :param width: the width of the slider
        :param height: the height of the slider
        :param percentage: the percentage of the bar filled (ex. 60 is 60%)
        :return: A slider class
        """
        # Create the button
        return slider(self.display, x, y, width, height, percentage)

    def create_dropbox(self, x, y, width, height, textList, initialText=None):
        """
        creates an dropbox with the provided values
        :param x: the x coordinate of the dropbox
        :param y: the y coordinate of the dropbox
        :param width: the width of the dropbox
        :param height: the height of the dropbox
        :param percentage: the percentage of the bar filled (ex. 60 is 60%)
        :return: A dropbox class
        """
        font = pg.font.Font(self.font, int(width))
        # Create the dropBox
        return dropBox(self.display, x, y, width, height, font, textList, initialText)


    def update_menu_resolution(self):
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        # initialize menu, game, and database objects
        self.main_menu = MainMenu(self)
        self.options_menu = OptionMenu(self)
        self.profile = Profile(self)
        self.ConnectFour = ConnectFour(self)
        self.LoadingScreen = LoadingScreen(self)
        self.Leaderboard = Leaderboard(self)

        self.current_screen = MainMenu(self)